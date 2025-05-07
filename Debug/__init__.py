import DaiCCore
import readline # optional, will allow Up/Down/History in the console
import code

def iter_shell():
    variables = globals().copy()
    variables.update(locals())
    shell = code.InteractiveConsole(variables)
    shell.interact()

DaiCCore.register("Debug", "Debug plugin that load a python intercative shell", iter_shell)
