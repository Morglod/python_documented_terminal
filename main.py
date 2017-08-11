import inspect
import termcolor
import traceback

"""
Test methods
"""

def printX(x = 'a'):
    """
    prints x
    
    :param x: Any printable
    """
    print(x)

def sum(a, b):
    """ sum of two args """
    call('printX', a+b)
    return a + b

"""
Magic
"""

def func_meta(func, y = 'a'):
    arg_spec = inspect.getargspec(func)
    return {
        'doc': inspect.getdoc(func),
        'file': inspect.getsourcefile(func),
        'source': inspect.getsource(func),
        'module': inspect.getmodule(func),
        'args': arg_spec.args,
        'defaults': dict(zip(arg_spec.args[-len(arg_spec.defaults):], arg_spec.defaults)) if arg_spec.defaults != None else {}
    }

def call(name, *args):
    func = globals()[name]
    meta = func_meta(func)
    printable_args = [ "{0}={1}".format(arg[0], arg[1]) for arg in [ x if x[1] != None else [ x[0], meta['defaults'][x[0]] ] for x in map(None, meta['args'], args) ] ]
    print termcolor.colored(("\n".join([
        "call '{0}' with {1}".format(name, ' '.join(printable_args)),
        "---",
        meta['doc'],
        "function is defined at '{0}' file, in '{1}' module".format(meta['file'], meta['module']),
        meta["source"],
        "---"
    ])), "yellow")
    return func(*args)

""""""""""""""""""""""""""""""""""""""""""

class CLI:
    def __getattr__(self, attr):
        global call
        return lambda *args: call(attr, *args)
cli = CLI()

cli.printX(123) # same as call('printX', 123)

command = raw_input("> ")
while command != "exit":
    try:
        print eval(command)
    except: traceback.print_exc()
    command = raw_input("> ")
