import flask.views
from flask import Flask

app = Flask(__name__)

class View(flask.views.MethodView):
    def get(self):
        return 'Hello World!'

app.add_url_rule('/hi', 'main', view_func=View.as_view('main'))

if __name__ == '__main__':
    app.run(debug=True)