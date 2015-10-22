# ttycaster

A system for streaming terminal applications to the web

## Pre-requisites

In order to capture terminal output, `ttyrec` is needed locally. There is a NodeJS version floating around but it is flaky when it comes to non-trivial terminal output so the following native version is recommended:

    https://github.com/mjording/ttyrec

To install, just run `make` and then stick the `ttyrec` and `ttyplay` binaries on your PATH.

## Setting up Docker on the server

If your server already has Docker you can skip this section. Otherwise, to install Docker on your server simply run:

    curl https://get.docker.com/ | sh

If you dont want to curl the install script over https you can visit http://docs.docker.com/ for more installation methods. Once installed, you should be able to view the Docker daemon info:

    docker info

Go ahead and pull down the ttycaster image:

    docker pull dlacewell/ttycaster

## SSH Funnel Service

http://github.com/dustinlacewell/funneld is used connect SSH sessions to the ttycaster container. Install it with pip:

    pip install funneld

Install the `ttycaster-sh` shell somewhere like `/usr/bin/ttycaster-sh`. Then create a system user named `ttycaster` and set ttycaster-sh as the shell:

    useradd -s /usr/bin/ttycaster-sh ttycaster

Start funneld on whatever port you'd like and tell it to use the `ttycaster` user:

    funneld --port 2200 ttycaster

## Streaming

Now that Docker, funneld and ttycaster-sh have been setup, SSH connections should be accepted and routed new `ttycast` processes. Use the `ttycaster` script locally to stream your favorite terminal application:

    ttycaster yourserver.com:2200 /usr/bin/htop

## Index webservice

There is an extremely basic webservice available that features a simple page which lists any active streams. It features html links to those streams with the correct port which allows those without access to the server's `docker` command to discover the streams. It also parses the stream `advert` and displays it next to the link.

Run the index by running the following container on the server:

    docker run -d --name ttycaster-index --restart=always \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -p 9000:9000 -e HOSTNAME=yourserver.com
        dlacewell/ttycaster-index
