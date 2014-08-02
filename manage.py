from flask.ext.script import Manager

from application import app
from core.context import get_script_manager

app.app_context()
manager = get_script_manager()

@manager.command
def hello():
    print "hello"

if __name__ == "__main__":
    manager.run()