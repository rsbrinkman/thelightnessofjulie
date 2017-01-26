from flask import Flask, render_template, Response
from flask import request
import phue

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
  result = None
  state = request.args.get('state')
  if state == 'sleep':
    pass
  if state == 'snuggle':
    pass
  if state == 'cook':
    pass
  if state == 'dinner':
    pass
  if state == 'movie':
    pass
  if state == 'love':
    pass


  return render_template('index.html', result=result)

if __name__ == "__main__":
      app.run(debug=True)
