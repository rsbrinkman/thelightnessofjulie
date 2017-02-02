from flask import Flask, render_template, Response
from flask import request
from functools import wraps
import requests
import json
from phue import Bridge

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
  ip = request.args.get('ip')
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
  #change_lights(bri)
  print bri
  
  return render_template('index.html')

def change_lights(state, bri=None):
  b = Bridge('192.168.10.115')
  lights = b.get_light_objects('list')
  for light in lights:
    if state == 'dinner':
      light.on = True
      light.brightness = 100
      light.transition_time = TRANSITION
    if state == 'sleep':
      light.on = False
      light. transition_time = TRANSITION
    if state == 'cook':
      light.on = True
      light.brightness = 150
      light.transition_time = TRANSITION
    if state == 'snuggle':
      light.on = True
      light.brightness = 50
      light.transition_time = TRANSITION
    if state == 'love':
      light.on = True
      light.brightness = 20
      light.transition_time = TRANSITION
    if state == 'movie':
      light.on = True
      light.brightness = 30
      light.transition_time = TRANSITION
    if bri:
      light.on = True
      light.brightness = bri



@app.route("/settings")
@requires_auth
def get_ip():
  # Get Bridge IP
  resp = requests.get('https://www.meethue.com/api/nupnp').content
  result = json.loads(resp)
  ip = result[0]['internalipaddress']

  return render_template('settings.html', ip=ip)
if __name__ == "__main__":
      app.run(debug=True)
