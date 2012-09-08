#!/usr/bin/env python

import sys
import time
import subprocess
import optparse

def get_version():
    cmd = ['git','show']
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    result = p.wait()
    if result != 0:
        print >> sys.stderr, "Error executing %s" % ' '.join(cmd)
        return None
    return p.stdout.readlines()[0].split(' ')[1].strip()

def get_number_of_versions(version):
    # git log 9bfcfb14afefd80473d4028c24f6b5019ebc3a5b --format="%h"
    cmd = ['git','log', version, '--format="%at"']
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    result = p.wait()
    if result != 0:
        print >> sys.stderr, "Error executing %s" % ' '.join(cmd)
        return None
    lines = [ line for line in p.stdout.readlines() ]
    timestamp = int(lines[0].strip().replace('"','').replace("'",''))
    date_str = time.strftime('%A, %B %d, %Y', time.localtime(timestamp))
    return len(lines), date_str

def generate(filename):
    version = get_version()
    if version is None:
        return
    number, date = get_number_of_versions(version)
    if number is None:
        return
    msg = r"""var wlVersionMessage = "WebLab-Deusto r<a href=\"https://github.com/porduna/weblabdeusto/commits/%(version)s\">%(version_number)s</a> | Last update: %(date)s";""" % {
        'version'         : version,
        'version_number'  : number,
        'date'            : date,
    }
    if filename == '-':
        print msg
    else:
        open(filename, 'w').write(msg)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f','--file', dest='file', metavar='FILE', default=None, help='File where to write the code')
    options, args = parser.parse_args()
    if options.file is None:
        parser.error("FILE missing")
    else:
        generate(options.file)
