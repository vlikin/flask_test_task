import flask, functools

def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kargs):
        if 'username' in flask.session:
            return method(*args, **kargs)
        else:
            flask.flash('A login is required to see a page.')
            return flask.redirect(flask.url_for('login'))

    return wrapper