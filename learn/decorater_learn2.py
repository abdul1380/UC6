"""
https://realpython.com/primer-on-python-decorators/

explaining @ for decorator
"""


from datetime import datetime
from decorater_learn3 import do_twice


def not_during_the_night(func):
    def wrapper():
        if 7 <= datetime.now().hour < 22:
            func()
        else:
            pass  # Hush, the neighbors are asleep
    return wrapper

def say_whee():
    print("Whee!")

say_whee = not_during_the_night(say_whee)

def not_during_the_day(func):
    def wrapper():
        if datetime.now().hour < 7:
            func()
        else:
            pass  # Hush, the neighbors are asleep
    return wrapper

@not_during_the_day
def say_hi():
    print("hi!")

@do_twice
def say_lovely():
    print("lovely!")



if __name__ == '__main__':
    say_whee()
    say_hi()
    say_lovely()
   