import os

from gevent import monkey; monkey.patch_all()

from docker import Client

from bottle import route, run, template, static_file

hostname = os.environ["HOSTNAME"]
port = os.environ.get("VIRTUAL_PORT", "80")

client = Client(base_url="unix:///var/run/docker.sock")

with open('/static/index.html') as fh:
    T = fh.read()

class Stream(object):
    def __init__(self, name, advert):
        self.name = name
        self.advert = advert
        self.url = "http://{}.{}/".format(name, hostname)

def get_containers():
    containers = client.containers(filters=dict(status='running'))
    return filter(lambda c: 'dlacewell/ttycaster' == c["Image"], containers)

def get_env(info, name, default=None):
    config = info.get("Config")
    if not config: return default
    env = config.get("Env")
    if not env: return default
    for var in env:
        key, val = var.split("=")
        if key == name:
            return val
    return default

def get_streams():
    containers = get_containers()
    for c in containers:
        info = client.inspect_container(c["Id"])
        name = info["Name"][1:]
        advert = get_env(info, "ADVERT")
        yield Stream(name, advert)

@route('/')
def index():
    streams = get_streams()
    return template(T, streams=list(streams))

@route('/static/<filename:path>')
def assets(filename):
    return static_file(filename, root='/assets')

run(host='0.0.0.0', port=int(port), server='gevent')
