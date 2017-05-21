FROM python:3.5

ENV WORKON_HOME /usr/local/python-venvs
ENV GOPATH /usr/go/
ENV GOMAXPROCS 1

ADD servers /usr/src/servers

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y \
	autoconf automake libtool build-essential nodejs golang

RUN mkdir -p /usr/local/python-venvs \
   && mkdir -p /usr/go \
   && pip3 install vex \
   && vex --python=python3.5 -m bench pip install -U pip \
   && mkdir -p /var/lib/cache/pip \
   && vex bench pip --cache-dir=/var/lib/cache/pip install -r /usr/src/servers/requirements.txt \
   && vex bench pip freeze -r /usr/src/servers/requirements.txt \
   && curl -L -o /usr/local/bin/gosu https://github.com/tianon/gosu/releases/download/1.10/gosu-$(dpkg --print-architecture | awk -F- '{ print $NF }') \
   && chmod +x /usr/local/bin/gosu \
   && cd /usr/src/servers \
   && go build goecho.go \
   && go get github.com/golang/groupcache/lru \
   && go build gohttp.go

EXPOSE 25000

VOLUME /var/lib/cache
VOLUME /tmp/sockets

ENTRYPOINT ["/entrypoint"]

ADD entrypoint /entrypoint