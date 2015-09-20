import threading

class MyThread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num
    def run(self):
        print 'Soy el hilo %s', self.num

if __name__ == '__main__':
    print 'testing module threading'
    t1 = MyThread()
    t2 = MyThread()

    t1.run()
    t2.run()
