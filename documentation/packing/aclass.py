from clog import logger

class ClassA(object):
    """
    Basic example class implemented for demonstration purposes.
    """

    def __init__(self):
        logger.info('Initializing an instance of %s' % self.__class__.__name__)

    def __call__(self):
        logger.info('Call %s as a function' % self.__class__.__name__)

    def display(self):
        logger.info('Display method from class %s' % self.__class__.__name__)

    def __repr__(self):
        return "graphical class representation"
        
    def __str__(self):
        return "print class representation"
