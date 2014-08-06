from core.context import get_script_manager
from application import app

if __name__ == "__main__":
  with app.app_context():
    from core.script import *
    script_manager = get_script_manager()
    script_manager.run()

