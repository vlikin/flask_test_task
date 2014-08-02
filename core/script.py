from core.context import get_script_manager

script_manager = get_script_manager()

@script_manager.command
def hello():
    print "hello"