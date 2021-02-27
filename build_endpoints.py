from flask import Flask
from string import Template
import json

app = Flask(__name__)

@app.route('/')
def homepage():
    return """<h1>Hello world!</h1>"""

@app.route('/<some_place>')
def some_place_page(some_place):
    
    return json.dumps({"test":"frank"})




if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)