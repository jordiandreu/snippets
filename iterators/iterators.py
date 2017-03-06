import time

from itertools import cycle


def my_generator():

    files = ['filename01', 'filename02', 'filename03']
    srcs = ['YUV420', 'YUV422', 'YUV444']
    dsts = ['RGB', 'BGR']

    for f, s in zip (files, srcs):
        for d in dsts:
            yield f, s, d

#g = my_generator()

# try:
#     while True:
#         print "next: %s, %s, %s" % g.next()
#         time.sleep(0.1)
# except StopIteration, e:
#     print "Stop iteration found"


# try:
#     for i in g:
#         print i
#         time.sleep(0.1)
# except StopIteration, e:
#     print "Stop iteration found"

# try:
#     for i in cycle(g):
#         print i
#         time.sleep(0.1)
# except StopIteration, e:
#     print "Stop iteration found"


# def my_generator():
#     for i in range(5):
#         yield i



def cycle_iterator():
    g = my_generator()
    for i in cycle(g):
        print i
        time.sleep(1)

g = cycle_iterator()

#for i in g:
#    print i

print next(g)