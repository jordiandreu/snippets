class SingletonDecorator:
    def __init__(self,klass):
        self.klass = klass
        self.instance = None

    def __call__(self,*args,**kwds):
        if self.instance is None:
            self.instance = self.klass(*args,**kwds)
        return self.instance

#@SingletonDecorator
class Beamline(object):
    def __init__(self):
        print 'Initializing beamline instance of Beamline.'


def get_beamline():
    return Beamline()
