from core.context import get_script_manager
import core.lib as lib

script_manager = get_script_manager()

@script_manager.command
def drop_all():
  '''It drops all tables.'''
  lib.drop_all()

@script_manager.command
def init_db():
  '''It creates the initial database.'''
  lib.init_db()