import xmlrpclib
import sys

from gevent import pywsgi

from util import _get_type_name


class LabListener(object):
    """
    Class that will listen on a port for a labserver-initiated XMLRPC connection, and which will
    receive the commands themselves. It will essentially have the same interface as an ExperimentServer.
    """

    def __init__(self, listen_host, listen_port):
        super(LabListener, self).__init__()
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.server = pywsgi.WSGIServer((self.listen_host, self.listen_port), self.on_http_request)

        # For now we will not use a method registry because we will just forward any method.
        self.methods_registry = {
        }

    def on_http_request(self, environ, start_response):
        """
        This should be handled in a Greenlet. It just forwards the request and
        returns the response.
        :type environ: dict
        :type start_response: __builtin__.instancemethod
        :return:
        """
        if environ['REQUEST_METHOD'] == 'GET':
            start_response('200', [('Content-Type', 'text/html')])
            return ["This server accepts ExperimentServer-like methods"]

        input = environ.get('wsgi.input')
        raw_data = input.read()

        params, method_name = xmlrpclib.loads(raw_data)
        if method_name.startswith('Util.'):
            method_name = method_name[len('Util.'):]

        # We do not check that the method exists here.
        # if method_name not in self.methods_list:
        #     start_response('404', [('Content-Type', 'text/html')])
        #     return [xmlrpclib.dumps(xmlrpclib.Fault("Method not found", "Method not found"))]

        try:
            if method_name == 'test_bridge':
                result = params[0]
            else:
                # We will simply forward the request.
                result = self.forward_request(raw_data)
                return [result]
        except:
            start_response('500', [('Content-Type', 'text/html')])
            exc_type, exc_instance, _ = sys.exc_info()
            remote_exc_type = _get_type_name(exc_type)
            fault = xmlrpclib.Fault(remote_exc_type, repr(exc_instance.args))
            # TODO: Log errors
            # log.error(__name__, 'Error on %s' % method_name)
            # log.error_exc(__name__)
            return [xmlrpclib.dumps(fault)]

        start_response('200 OK', [('Content-Type', 'text/html')])
        content = xmlrpclib.dumps((result,))
        return [content]

    def forward_request(self, raw_data):
        print "FORWARDING REQUEST"

    def start(self):
        """
        Registers all experiment server - like methods and starts the XMLRPC server.
        :return:
        """
        return self.server.start()