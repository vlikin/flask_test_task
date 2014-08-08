from flask import g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.script import Manager as ScriptManager
from application import app


def get_script_manager():
  '''It initializes the script manager at once.'''
  script_manager = getattr(g, '_script_manager', None)
  if script_manager is None:
    script_manager = g._script_manager = ScriptManager(app)
  return script_manager