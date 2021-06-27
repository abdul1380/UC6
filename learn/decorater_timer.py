"""
The following @debug decorator will print the arguments a function is
 called with as well as its return value every time the function is called:

"""
import functools
import math
def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug

'''

The signature is created by joining the string representations of all the arguments.
 The numbers in the following list correspond to the numbered comments in the code:

1 Create a list of the positional arguments. Use repr() to get a nice string representing each argument.
2: Create a list of the keyword arguments. The f-string formats each argument as key=value where the !r specifier means that repr() is used to represent the value.
3: The lists of positional and keyword arguments is joined together to one signature string with each argument separated by a comma.
4: The return value is printed after the function is executed.
Lets see how the decorator works in practice by applying it to a simple function with one position and one keyword argument:
'''

@debug
def make_greeting(name, age=None):
    if age is None:
        return f"Howdy {name}!"
    else:
        return f"Whoa {name}! {age} already, you are growing up!"




if __name__ == '__main__':
    make_greeting("Benjamin")
    print()
    make_greeting("Benjamin", age = 21)