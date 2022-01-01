import functools

void = type(None)

def matches(signature, args):
    if (len(signature) != len(args)): return False
    for type_, arg in zip(signature, args):
        if not isinstance(arg, type_): return False
    return True

def UniqueSignature(returnTolerance=False):
    def handler(func):
        @functools.wraps(func)
        def manager(*args, **kwargs):
            annot = func.__annotations__
            if not 'return' in annot.keys():
                returnType = void
                signature = tuple(annot.values())
            else:
                returnType = annot['return']
                signature = tuple(annot.values())[:-1]
            if matches(signature, args):
                returned = func(*args, **kwargs)
                if returnTolerance or isinstance(returned, returnType): return None
                else: raise Exception("Returned value does not match the precised one")
            else: raise Exception(f"Invalid arguments, does not match the signature of \"{func.__name__}\" which have an unique signature")
        return manager
    return handler

@UniqueSignature()
def test(x : int, y : int):
    """
    Ceci est ma docstring
    """
    print(x, y)
    return True


print(test.__annotations__)