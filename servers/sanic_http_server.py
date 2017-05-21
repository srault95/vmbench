
import sys
import argparse

from sanic import Sanic
from sanic import response

app = Sanic(__name__)

def abort(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

@app.route("/<msize>")
async def index(request, msize=1024):
    _msize = 1024
    try:
        _msize = int(msize)
    except:
        pass
    answer = 'X' * _msize
    return response.text(answer)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', default='sanic', action='store')
    parser.add_argument('--addr', default='127.0.0.1:25000', type=str)
    parser.add_argument('--worker', default='1', type=int)
    args = parser.parse_args()

    if args.type:
        #print('using {} loop: {!r}'.format('uvloop', app.loop))
        print('using {} HTTP server'.format('sanic'))

    addr = args.addr.split(':')
    addr[1] = int(addr[1])
    addr = tuple(addr)

    print('serving on: {}'.format(addr))
    
    app.run(host="0.0.0.0", port=addr[1],
            backlog=100,
            log_config=None,
            workers=args.worker)
