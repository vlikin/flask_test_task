from flask import g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from application import app

def get_db():
    db = getattr(g, '_database.', None)
    if db is None:
        db = g._database = SQLAlchemy(app)
    return db

@app.teardown_appcontext
def teardpown_db(exception):
    pass

def get_login_manager():
    login_manager = getattr(g, '_login_manager.', None)
    if login_manager is None:
        login_manager = LoginManager()
        login_manager.init_app(app)
    else:
        return login_manager

def init_db():
    from core.models.user import User
    db = get_db()
    db.drop_all()
    db.create_all()
    ##return
    admin = User('admin', 'admin@example.com')
    guest = User('guest', 'guest@example.com')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()

    return db
