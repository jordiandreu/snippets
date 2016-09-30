import logging


class MyHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        #fmt = '%(asctime)s %(filename)-18s %(levelname)-8s: %(message)s'
        #fmt_date = '%Y-%m-%dT%T%Z'
        fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        #formatter = logging.Formatter(fmt, fmt_date)
        formatter = logging.Formatter(fmt)
        self.setFormatter(formatter)

#if __name__ == '__main__':

#    log = logging.getLogger(__name__) #or any string
#    log.setLevel('DEBUG')
#    log.addHandler(MyHandler())

    # 'application' code
#    log.debug('debug message')
##    log.info('info message')
#    log.warn('warn message')
#    log.error('error message')
#    log.critical('critical message')

# This has to be added to each module which use the custom logger
# log = logging.getLogger('root') or __name__
# log.setLevel('DEBUG')
# log.addHandler(mylogging.MyHandler())
