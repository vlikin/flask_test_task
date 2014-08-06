import flask, flask.views
from flask.ext.login import login_required
import os

class Remote(flask.views.MethodView):

    @login_required
    def get(self):
        return flask.render_template('remote.html')

    def post(self):
        result = eval(flask.request.form['expression'])
        flask.flash(result)
        return self.get()