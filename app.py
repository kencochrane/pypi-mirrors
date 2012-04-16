from flask import Flask, render_template
from utils import get_page_data

app = Flask(__name__)

@app.route('/')
def index():
    context = get_page_data()
    return render_template('index.html', **context)

if __name__ == '__main__':
    params = {"debug": True,
              "host":"0.0.0.0",}

    app.run(**params)