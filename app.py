import flask, flask.views
from flask import Flask
import os
import functools

app = Flask(__name__)
app.secret_key = 'key'

def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kargs):
        if 'username' in flask.session:
            return method(*args, **kargs)
        else:
            flask.flash('A login is required to see a page.')
            return flask.redirect(flask.url_for('index'))

    return wrapper

class Index(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')

    def post(self):
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return self.get()
        users = {
            'viktor': 'viktor',
            'admin': 'admin'
        }
        required = ['username', 'password']
        for field in required:
            if field not in flask.request.form:
                flask.flash('Error: {0} is required'.format(field))
                return flask.redirect(flask.url_for('index'))
        username = flask.request.form['username']
        password = flask.request.form['password']
        if username in users and users[username] == password:
            flask.session['username'] = username
        else:
            flask.flash('Username does not exists or incorrect password.');
        return flask.redirect(flask.url_for('index'))

class Remote(flask.views.MethodView):

    @login_required
    def get(self):
        return flask.render_template('remote.html')

    @login_required
    def post(self):
        result = eval(flask.request.form['expression'])
        flask.flash(result)
        return self.get()

class Music(flask.views.MethodView):

    @login_required
    def get(self):
        songs = os.listdir('static/files/music/')
        print songs
        return flask.render_template('music.html', songs=songs)

app.add_url_rule('/', view_func=Index.as_view('index'), methods=['GET', 'POST'])
app.add_url_rule('/remote', view_func=Remote.as_view('remote'), methods=['GET', 'POST'])
app.add_url_rule('/music', view_func=Music.as_view('music'), methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)