from decorater_learn3 import do_twice
from decorater_learn3 import decorator

@do_twice
def greet(name):
    print(f"Hello {name}")

@do_twice
def return_greeting(name):
    print("Creating greeting")
    return f"Hi {name}"

@decorator
def say(anything):
    print("ANYTHING",anything)

if __name__ == '__main__':
    greet("world")
    s= return_greeting("Abdul")
    print(s)
    c =say("pakistan")
    print(c)
    
    