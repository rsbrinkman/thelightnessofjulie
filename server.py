import db
from flask import Flask, render_template, Response, jsonify
from flask import request

from functools import wraps
import json
from phue import Bridge
import logging
import requests

logging.basicConfig()

USERNAME = 'aREks51uQO6TPSP-T94zMFYDMA0WCuJDXmBWJM7Q'
TRANSITION = 1000
app = Flask(__name__)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'lux' and password == 'felicitas'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route("/", methods=['GET', 'POST'])
@requires_auth
def index():
  # Get lights
  state = request.args.get('state')
  if state == 'sleep':
    change_lights('sleep')
  if state == 'snuggle':
    change_lights('snuggle')
  if state == 'cook':
    change_lights('cook')
  if state == 'dinner':
    change_lights('dinner')
  if state == 'movie':
    change_lights('movie')
  if state == 'love':
    change_lights('love')

  return render_template('index.html')

@app.route("/change/<bri>", methods=['GET', 'POST'])
def slide_change(bri):
  bri = int(bri)
  if bri == 0:
    bri = 'off'
  change_lights('manual', bri)

  return render_template('index.html')

def change_lights(state, bri=None):
  settings = db.read_settings()
  b = Bridge(settings['ip'])
  lights = b.get_light_objects('list')
  for light in lights:
    if state == 'dinner':
      light.on = True
      light.brightness = int(settings['dinner'])
      light.transition_time = TRANSITION
    if state == 'sleep':
      light.on = False
      light.transition_time = TRANSITION
    if state == 'cook':
      light.on = True
      light.brightness = int(settings['cook'])
      light.transition_time = TRANSITION
    if state == 'snuggle':
      light.on = True
      light.brightness = int(settings['snuggle'])
      light.transition_time = TRANSITION
    if state == 'love':
      light.on = True
      light.brightness = int(settings['love'])
      light.transition_time = TRANSITION
    if state == 'movie':
      light.on = True
      light.brightness = int(settings['movie'])
      light.transition_time = TRANSITION
    if state == 'manual' and bri:
      if bri == 'off':
        light.on = False
      else:
        light.on = True
        light.brightness = bri

@app.route("/update_lightness", methods=['POST', 'GET'])
@requires_auth
def get_update_bri():
  data = request.form.to_dict()
  db.write_settings(data)
  settings = db.read_settings() 
  return render_template('update_lightness.html', settings=settings)

@app.route("/update_ip", methods=['POST', 'GET'])
@requires_auth
def update_ip():
  settings = db.read_settings()
  settings_ip = settings['ip']
  ip = request.args.get('ip')
  if ip:
    if ip != settings['ip']:
      data = {'ip': ip}
      db.write_settings(data)
    
  return 'done'

@app.route("/get_settings")
@requires_auth
def get_settings():
  
  return jsonify(db.read_settings())

@app.route("/settings", methods=['POST', 'GET'])
@requires_auth
def get_ip():
  # Get Bridge IP
  resp = requests.get('https://www.meethue.com/api/nupnp').content
  resp = list(resp)
  try:
    result = json.loads(resp)
    ip = result[0]['internalipaddress']
    settings = db.read_settings()
  except:
    settings = 'no bridge' 
    ip = 'no bridge'

  return render_template('settings.html', ip=ip, settings=settings)
'''
@app.route("/update_ip/", methods=['POST', 'GET'])
@requires_auth
def update_ip():
  settings = db.read_settings()
  settings_ip = settings['ip']
  updated = False
  ip = request.args.get('ip')
  if ip:
    if ip != settings['ip']:
      data = {'ip': ip}
      db.write_settings(data)
      updated = True
  else:
    updated = 'no_bridge'
  return render_template('set_ip.html', ip=ip, updated=updated)
'''
if __name__ == "__main__":
      app.run(host='0.0.0.0', debug=True)
