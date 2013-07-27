from flask import Flask, render_template, Response
from utils import get_page_data, get_json_data

app = Flask(__name__)

@app.route('/')
def index():
    context = get_page_data()
    return render_template('index.html', **context)

@app.route('/data.json')
def json_data():
    return Response(get_json_data(),mimetype='application/json')

if __name__ == '__main__':
    params = {"debug": True,
              "host":"0.0.0.0",}

    app.run(**params)