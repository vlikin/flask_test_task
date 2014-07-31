import flask, flask.views
import settings

class Login(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')

    def post(self):
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return self.get()
        required = ['username', 'password']
        for field in required:
            if field not in flask.request.form:
                flask.flash('Error: {0} is required'.format(field))
                return flask.redirect(flask.url_for('login'))
        username = flask.request.form['username']
        password = flask.request.form['password']
        if username in settings.users and settings.users[username] == password:
            flask.session['username'] = username
        else:
            flask.flash('Username does not exists or incorrect password.');
        return flask.redirect(flask.url_for('index'))
