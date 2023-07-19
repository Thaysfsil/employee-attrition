import inspect
import types

def mainify(obj, warn_if_exist=True):
    ''' If obj is not defined in __main__ then redefine it in main. Allows dill 
    to serialize custom classes and functions such that they can later be loaded
    without them being declared in the load environment.

    Parameters
    ---------
    obj           : Object to mainify (function or class instance)
    warn_if_exist : Bool, default True. Throw exception if function (or class) of
                    same name as the mainified function (or same name as mainified
                    object's __class__) was already defined in __main__. If False
                    don't throw exception and instead use what was defined in
                    __main__. See Limitations.
    Limitations
    -----------
    Assumes `obj` is either a function or an instance of a class.                
    ''' 
    if obj.__module__ != '__main__':                                                
        
        import __main__       
        is_func = True if isinstance(obj, types.FunctionType) else False                                            
        
        # Check if obj with same name is already defined in __main__ (for funcs)
        # or if class with same name as obj's class is already defined in __main__.
        # If so, simply return the func with same name from __main__ (for funcs)
        # or assign the class of same name to obj and return the modified obj        
        if is_func:
            on = obj.__name__
            if on in __main__.__dict__.keys():
                if warn_if_exist:
                    raise RuntimeError(f'Function with __name__ `{on}` already defined in __main__')
                return __main__.__dict__[on]
        else:
            ocn = obj.__class__.__name__
            if ocn  in __main__.__dict__.keys():
                if warn_if_exist:
                    raise RuntimeError(f'Class with obj.__class__.__name__ `{ocn}` already defined in __main__')
                obj.__class__ = __main__.__dict__[ocn]                
                return obj
                                
        # Get source code and compile
        source = inspect.getsource(obj if is_func else obj.__class__)
        compiled = compile(source, '<string>', 'exec')                    
        # "declare" in __main__, keeping track which key of __main__ dict is the new one        
        pre = list(__main__.__dict__.keys()) 
        exec(compiled, __main__.__dict__)
        post = list(__main__.__dict__.keys())                        
        new_in_main = list(set(post) - set(pre))[0]
        
        # for function return mainified version, else assign new class to obj and return object
        if is_func:
            obj = __main__.__dict__[new_in_main]            
        else:            
            obj.__class__ = __main__.__dict__[new_in_main]
                
    return obj