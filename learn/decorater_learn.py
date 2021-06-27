"""
https://realpython.com/primer-on-python-decorators/
"""


def be_awesome(name):
    return f"Yo {name}, together we are the awesomest!"

def greet_bob(greeter_func):
    return greeter_func("Bob")

def parent(num):
    def first_child():
        return "Hi, I am Emma"

    def second_child():
        return "Call me Liam"

    if num == 1:
        return first_child
    else:
        return second_child
    

def my_decorator(func):
    def wrapper():
        print("Something happening before function is called.")
        func()
        print("Something happening after the function is called.")
    return wrapper

def say_whee():
    print("Whee!")

say_whee = my_decorator(say_whee)

if __name__ == '__main__':
    r = greet_bob(be_awesome) # be_awesome is named without parantheis
    # it means it wont execute, only a reference to be_awesome is passed
    # greet_bob() iswritten with paranthesis so it will run as usual
    print(r) # Yo Bob, together we are the awesomest!
    r =parent(1)
    print()   # <function parent.<locals>.first_child at 0x000002717FCA18C8>
            # cryptic output simply means that r refers to first_child() function inside of parent()
    print(r()) # Hi, I am Emma
    
    say_whee() # bcoz of decoration at line 35 say_whee now points out to wrapper() inner function