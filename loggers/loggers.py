#!/bin/env

# IMPORTS SECTION
#================
import logging


# LOGGING CONFIGURATION
#======================
# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')


# CLASS DEFINITION
#================
class ClassA(object):
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
        
class ClassB(object):
    def __init__(self):
        logger.info('Initializing an instance of %s' % self.__class__.__name__)

    def __call__(self):
        logger.info('Call %s as a function' % self.__class__.__name__)

    def display(self):
        logger.info('Display method from class %s' % self.__class__.__name__)

class ClassAB(ClassA, ClassB):
    def __init__(self):
        super(ClassAB, self).__init__()
        logger.info('Initializing an instance of %s' % self.__class__.__name__)

    def __call__(self):
        logger.info('Call %s as a function' % self.__class__.__name__)

    def display(self):
        logger.info('Display method from class %s' % self.__class__.__name__)


# MAIN EXECUTION BLOCK
#=====================
if __name__ == '__main__':

    A = ClassA()
    B = ClassB()
    AB = ClassAB()
    
    A()
    B()
    
    ClassA().display()
    ClassB().display()

    A
    print A
