
import argparse
from gevent.pywsgi import WSGIServer
from flask import Flask, current_app, request

application = Flask(__name__)

@application.route('/<int:msize>')
def home(msize=1024):
    answer = 'X' * msize
    response = current_app.response_class(answer,
                            mimetype='text/plain')
    response.status_code = 200    
    response.make_conditional(request)
    return response

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', default='gevent+flask', action='store')
    parser.add_argument('--addr', default='0.0.0.0:25000', type=str)
    args = parser.parse_args()

    if args.type:
        print('using {} HTTP server'.format('gevent+flask'))

    addr = args.addr.split(':')
    addr[1] = int(addr[1])
    addr = tuple(addr)

    print('serving on: {}'.format(addr))
    
    try:
        WSGIServer(('0.0.0.0', addr[1]), application,
                   backlog=100, log=None).serve_forever()
    except KeyboardInterrupt:
        pass
    
