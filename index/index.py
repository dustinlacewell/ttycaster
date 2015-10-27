import os

from gevent import monkey; monkey.patch_all()

from docker import Client

from bottle import route, run, template

hostname = os.environ["HOSTNAME"]
port = os.environ.get("PORT", "9000")

client = Client(base_url="unix:///var/run/docker.sock")

T = """

<html>
  <body>
    % if not streams:
    <h1>No streams are active.</h1>
    % else:
    <h1>Current Streams:</h1>
    <ul>
      % for stream in streams:
      <li>
        <a href="{{stream.url}}">{{stream.name}}</a>
        <span class="advert">{{stream.advert}}</span>
      </li>
      % end
    </ul>
    % end
  </body>
</html>
"""

class Stream(object):
    def __init__(self, name, port, advert):
        self.name = name
        self.port = port
        self.advert = advert
        self.url = "http://{}:{}/".format(hostname, port)

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

def get_port(info, port):
    settings = info.get('NetworkSettings')
    if not settings: return 0
    ports = settings.get('Ports')
    if not ports: return 0
    for key, value in ports.items():
        number, proto = key.split('/')
        if str(number) == str(port):
            return value[0]["HostPort"]

def get_streams():
    containers = get_containers()
    for c in containers:
        info = client.inspect_container(c["Id"])
        name = get_env(info, "NAME")
        port = get_port(info, 9000)
        advert = get_env(info, "ADVERT")
        yield Stream(name, port, advert)

@route('/')
def index():
    streams = get_streams()
    return template(T, streams=list(streams))

run(host='0.0.0.0', port=int(port), server='gevent')
