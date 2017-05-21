
import sys
import argparse
import asyncio

from aiohttp.web import Application, Response, StreamResponse, run_app

async def index(request):
    resp = StreamResponse()
    msize = 1024
    try:
        msize = int(request.match_info.get('msize', '1024'))
    except:
        pass
    #answer = ('Hello, ' + name).encode('utf8')
    answer = b'X' * msize    
    resp.content_length = len(answer)
    resp.content_type = 'text/plain'
    await resp.prepare(request)
    resp.write(answer)
    await resp.write_eof()
    return resp

def abort(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

async def init(loop):
    app = Application()
    app.router.add_get('/{msize}', index)
    return app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', default='asyncio+aiohttp', action='store')
    parser.add_argument('--addr', default='127.0.0.1:25000', type=str)
    args = parser.parse_args()

    if args.type:
        parts = args.type.split('+')
        if len(parts) > 1:
            loop_type = parts[0]
            server_type = parts[1]
        else:
            server_type = args.type

        if server_type in {'aiohttp', 'httptools'}:
            if not loop_type:
                loop_type = 'asyncio'
        else:
            loop_type = None

        if loop_type not in {'asyncio', 'uvloop'}:
            abort('unrecognized loop type: {}'.format(loop_type))

        if server_type not in {'aiohttp', 'httptools'}:
            abort('unrecognized server type: {}'.format(server_type))

        if loop_type:
            if loop_type == "uvloop":
                import uvloop
                loop = uvloop.new_event_loop()
            else:
                loop = globals()[loop_type].new_event_loop()
        else:
            loop = None

        print('using {} loop: {!r}'.format(loop_type, loop))
        print('using {} HTTP server'.format(server_type))

    if loop:
        asyncio.set_event_loop(loop)
        loop.set_debug(False)

    unix = False
    if args.addr.startswith('file:'):
        unix = True
        addr = args.addr[5:]
    else:
        addr = args.addr.split(':')
        addr[1] = int(addr[1])
        addr = tuple(addr)

    print('serving on: {}'.format(addr))

    if loop:
        try:
            loop = asyncio.get_event_loop()
            app = loop.run_until_complete(init(loop))
            run_app(app, host="0.0.0.0", port=addr[1], 
                    access_log=None,
                    backlog=100 #default loop.create_server
                    )
        finally:
            loop.close()

