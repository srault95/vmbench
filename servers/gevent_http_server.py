
import argparse
from gevent.pywsgi import WSGIServer
from werkzeug.wrappers import Request, Response

def application(environ, start_response):
    request = Request(environ)
    msize = 1024
    try:
        msize = int(request.path.split('/')[-1])
    except:
        pass
    answer = 'X' * msize
    response = Response(answer, content_type='text/plain')
    return response(environ, start_response)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', default='gevent+wsgi', action='store')
    parser.add_argument('--addr', default='0.0.0.0:25000', type=str)
    args = parser.parse_args()

    if args.type:
        print('using {} HTTP server'.format('gevent+wsgi'))

    addr = args.addr.split(':')
    addr[1] = int(addr[1])
    addr = tuple(addr)

    print('serving on: {}'.format(addr))
    
    try:
        WSGIServer(('0.0.0.0', addr[1]), application,
                   backlog=100, log=None).serve_forever()
    except KeyboardInterrupt:
        pass
    
