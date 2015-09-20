import loggers

# LOGGING CONFIGURATION
# ---------------------
# create logger
logger = loggers.getLogger(__name__)
logger.setLevel(loggers.DEBUG)

# create console handler and set level to debug
ch = loggers.StreamHandler()
ch.setLevel(loggers.DEBUG)

# create formatter
formatter = loggers.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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

