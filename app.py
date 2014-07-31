import flask, flask.views
from flask import Flask
import os

app = Flask(__name__)
app.secret_key = 'key'

class View(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')

    def post(self):
        result = eval(flask.request.form['expression'])
        flask.flash(result)
        return self.get()

app.add_url_rule('/', 'main', view_func=View.as_view('main'), methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)