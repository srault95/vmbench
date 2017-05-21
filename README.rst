Network Server Performance Benchmarking Toolbench
=================================================

This is a simple collection of scripts intended to benchmark the basic
network performance of a variety of server frameworks.

The servers are run inside a Docker container for environment stability,
so to use this toolbench you need a reasonably recent Docker.

HTTP Servers Tested
-------------------

- HTML Report : http://espace-groupware.com/docs/vmbench/report-http.html
- Json Report : http://espace-groupware.com/docs/vmbench/report-http.json

===================  ====================  =============
Product              Benchmark Key          Comments  
===================  ====================  =============
`AioHTTP/asyncio`_   http-asyncio-aiohttp
`AioHTTP/uvloop`_    http-uvloop-aiohttp
`Sanic`_             http-sanic            uvloop
`Sanic`_             http-sanic-workers    uvloop / multi-workers
`Gevent/WSGI`_       http-gevent-wsgi
`Gevent/Flask`_      http-gevent-flask 
`Node.js`_           http-nodejs           http module - Node.js 0.10.29
`Golang`_            http-golang           net/http - Golang 2:1.3.3
===================  ====================  =============

.. _`AioHTTP/asyncio`: http://aiohttp.readthedocs.io
.. _`AioHTTP/uvloop`: https://github.com/MagicStack/uvloop
.. _`Sanic`: https://github.com/channelcat/sanic
.. _`Gevent/WSGI`: http://gevent.org/
.. _`Gevent/Flask`: http://flask.pocoo.org
.. _`Node.js`: https://nodejs.org/
.. _`Golang`: https://golang.org/

Screenshots
-----------

Requests/Seconds
::::::::::::::::

.. image:: http://espace-groupware.com/docs/vmbench/http-report-requests.png
   :align: center

Latency
:::::::

.. image:: http://espace-groupware.com/docs/vmbench/http-report-latency.png
   :align: center


Test Server Description
-----------------------

Information complémentaire sur les différences obtenues par rapport au test original sur https://magic.io/blog/uvloop-blazing-fast-python-networking/http-bench.html

- magic.io: Linux 4.4.5 (Ubuntu 16.04, x86_64) on Intel(R) Xeon(R) CPU E5-1620 v2 @ 3.70GHz

- Me: Linux 4.4.0-57-generic (Docker/Debian 8.7, x86_64) on Intel(R) Xeon(R) CPU W3520 @ 2.67GHz

My server: (https://www.soyoustart.com/fr/offres/142sys4.xml)

- OVH - So you Start - 16G ECC - Intel(R) Xeon(R) CPU W3520 @ 2.67GHz 4c/8t SoftRaid 2x2 To

Installation
------------

Requirements:

- Docker (tested on Docker 17.04.0-ce / Ubuntu 16.04)
- Python 3 (tested on Python 3.5.3 64bits)
- Wrk (tested on Wrk 4.0.1)
- Numpy

::

   $ apt-get install -y python3-numpy wrk

   $ git clone -b add_features https://github.com/srault95/vmbench
   
   $ cd vmbench

   # Build the docker image containing the servers 
   # being tested by running   
   $ ./build.sh

Running Tests
-------------

::

   # The benchmarks can then be ran with
   $ ./run_benchmarks --help
   
   # Example for run all http tests:
   $ ./run_benchmarks --save-html report-http.html --benchmarks http-*

   # Run one test for Sanic Http Server with duration (30sec) 
   # and concurency (300)
   $ ./run_benchmarks --save-html report-http.html \
      --benchmarks http-uvloop-aiohttp \
      --duration 30 --concurrency-levels 300

Debug
-----

Pour la mise au point des services à tester, vous pouvez lancement manuellement 
le container Docker comme le ferait le script ``run_benchmark``

Avec un volume vers $PWD/servers:/usr/src/servers, vous pouvez éditer les services 
sans relancer le build de l'image Docker.

::
   
   # Update docker image: magic/benchmark
   $ ./build.sh

   $ docker run --rm -it -p 25000:25000 -e UID=0 -e GID=0 \
      -v $PWD/servers:/usr/src/servers \
      -v $PWD/.cache:/var/lib/cache \
      -v $PWD/sockets:/tmp/sockets magic/benchmark \
      vex bench python /usr/src/servers/sanic_http_server.py --addr=0.0.0.0:25000 --worker=1

   # Go to navigator and open http://YOUR_IP:25000/[MSIZE]
   # http://YOUR_IP:25000/1024

   # Or run the http_client/echo_client
   $ ./http_client --output-format=json --addr=127.0.0.1:25000 \
      --msize=1024 --concurrency=300 --duration=30
   
Python Libraries Version
------------------------

::

   $ docker run --rm -it magic/benchmark vex bench pip freeze

   aiofiles==0.3.1
   aiohttp==2.0.7
   appdirs==1.4.3
   async-timeout==1.2.1
   chardet==3.0.3
   click==6.7
   curio==0.4
   Flask==0.12.2
   gevent==1.2.1
   greenlet==0.4.12
   httptools==0.0.9
   itsdangerous==0.24
   Jinja2==2.9.6
   MarkupSafe==1.0
   multidict==2.1.5
   packaging==16.8
   pyparsing==2.2.0
   sanic==0.5.4
   six==1.10.0
   tornado==4.5.1
   Twisted==16.1.1
   ujson==1.35
   uvloop==0.8.0
   websockets==3.3
   Werkzeug==0.12.2
   yarl==0.10.2
   zope.interface==4.4.1
         
