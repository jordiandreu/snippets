import timeit

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def costly_func(lst): 
    return map(lambda x: x^2, lst)


class Timed(object):
    def function(self,lst):
        return costly_func(lst)

if __name__ == "__main__":

    args_list = range(10)

# Timing a module function using a . The wrapper function is used to pass the
# arguments.
    wrapped = wrapper(costly_func, args_list)
    print timeit.timeit(wrapped, number=1000)
    
# Timing a member function:
    t = timeit.Timer("to.function(args_list)", "from __main__ import Timed, "
                                               "args_list; to=Timed()")
    print t.timeit(number=1000)
