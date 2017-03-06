import logging
logging.basicConfig(level=logging.DEBUG)


class ClassA(object):
    """
    Basic example class implemented for demonstration purposes.
    """

    def __init__(self):
        logging.getLogger().info('Initializing an instance of %s' % self.__class__.__name__)

    def __call__(self):
        logging.getLogger().info('Call %s\ as a function' % self.__class__.__name__)

    def display(self):
        logging.getLogger().info('Display method from class %s' % self.__class__.__name__)

    def __repr__(self):
        return "graphical class representation"
        
    def __str__(self):
        return "print class representation"


if __name__ == "__main__":
    a = ClassA()
