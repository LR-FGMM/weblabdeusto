import os
import time
import traceback
import subprocess

import requests

from wcloud import app as flask_app
from wcloud.tasks.celery_app import celery_app

DEBUG = True

@celery_app.task(bind=True)
def start_weblab(self, dirname, wait):
    stdout_path = os.path.join(dirname, "stdout.txt")
    stderr_path = os.path.join(dirname, "stderr.txt")

    print "Starting instance: %s" % dirname,

    help_process = subprocess.Popen(['weblab-admin', 'create', '--help'])
    help_process.wait()
    if help_process.poll() != 0:
        raise Exception("weblab-admin not installed. Are you running on a development environment?")

    process = subprocess.Popen(['nohup','weblab-admin', 'start', dirname],
                stdout = open(stdout_path, 'w+', 0),
                stderr = open(stderr_path, 'w+', 0),
                stdin  = subprocess.PIPE)

    print "[done]"

    variables = {}
    execfile(os.path.join(dirname, 'debugging.py'), variables, variables)
    ports = variables['PORTS']['json']
    urls = [ 'http://localhost:%s/weblab/json/' % port for port in ports ]

    if wait:
        wait_process(urls, stdout_path, stderr_path)

    errors = open(stderr_path).read()
    print "[dbg] Stderr: " + errors
    print "[dbg:END OF STDERR]"

    logs = open(stdout_path).read()
    print "[dbg] Stdout: " + errors
    print "[dbg:END OF STDOUT]"
    return

def _test_weblab(urls):
    for url in urls:
        try:
            r = requests.get(url, proxies = {})
        except:
            if DEBUG:
                traceback.print_exc()
            return False
        else:
            if r.status_code != 200:
                return False
    return True

def wait_process(urls, stdout_path, stderr_path):
    """
    Checks that the Process is running for the number of seconds specified in the configuration.
    If within that time the process stops running, an exception is thrown.
    """

    print "Waiting for process to start and stay..."

    time_to_wait = flask_app.config.get("WEBLAB_STARTUP_TIME", 20)

    start_time = time.time()

    # Wait for some seconds to start with. Apparently POPEN() did not immediately start the process in some instances.
    # This meant than when we ran the following check, it was mistakenly reported as a failure.
    # TODO: The 4 here is a magic number. This should probably be improved. Ideally, with a better way to detect
    # failures.
    time.sleep(7)

    while (time.time() - start_time) < time_to_wait:
        if _test_weblab(urls):
            break
        time.sleep(0.3)

    if not _test_weblab(urls):
        print open(stdout_path).read()
        print open(stderr_path).read()
        raise Exception("Weblab was apparently not started successfully (not running after %f seconds)" % (time.time() - start_time))

def stop_weblab(dirname):
    print "Stopping instance: %s" % dirname,
    try:
        result = subprocess.check_output(['weblab-admin', 'stop', dirname])
    except subprocess.CalledProcessError:
        return False

    print "[done]"
    return True


@celery_app.task(bind=True)
def start_redis(self, directory, config_file, port):
    stdout_path = os.path.join(directory, "stdout_redis_%s.txt" % port)
    stderr_path = os.path.join(directory, "stderr_redis_%s.txt" % port)

    process_args = ['nohup','redis-server', os.path.join(directory, config_file) ]
    print "Calling", process_args,"from",os.getcwd()
    process = subprocess.Popen(process_args,
                stdout = open(stdout_path, 'w+', 0),
                stderr = open(stderr_path, 'w+', 0))
    time.sleep(2)

