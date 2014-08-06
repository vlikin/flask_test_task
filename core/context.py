from flask import g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.script import Manager as ScriptManager
from application import app

def get_db():
  '''It initializes the database connection at once.'''
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = SQLAlchemy(app)
  return db

@app.teardown_appcontext
def teardpown_db(exception):
  '''It closes the site database connection.'''
  pass

def get_login_manager():
  '''It initializes the login manager at once.'''
  login_manager = getattr(g, '_login_manager', None)
  if login_manager is None:
    login_manager = LoginManager()
    login_manager.init_app(app)

  return login_manager

def get_script_manager():
  '''It initializes the script manager at once.'''
  script_manager = getattr(g, '_script_manager', None)
  if script_manager is None:
    script_manager = g._script_manager = ScriptManager(app)
  return script_manager