import argparse
import logging
import logging.handlers

LOGFILE_NAME = 'template.log'
MAX_LOGSIZE = 1000
MAX_LOGFILES = 5


def get_logger(sconsole, sfile, rotatory=False):

    desc = 'description'
    epil = 'epilog.'
    lvls = ['debug', 'info', 'warning', 'error', 'critical']

    parser = argparse.ArgumentParser(description=desc, epilog=epil)
    parser.add_argument('--log-level', type=str, choices=lvls,
                        help='help', default='debug')
    parser.add_argument('--log-dir', type=str,
                        help='help', default='./')

    args = parser.parse_args()
    loglevel = args.log_level
    logdir = args.log_dir

    # get loglevel
    level = getattr(logging, loglevel.upper(), None)
    if not isinstance(level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    # create logger object
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    # create formatter object
    fmt = '%(asctime)s %(levelname)10s [%(name)s]: %(message)s'
    formatter = logging.Formatter(fmt)

    if sconsole:
        # create stream handler (console)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if sfile:
        # create file handler (logfile)
        fh = logging.FileHandler(logdir + LOGFILE_NAME)
        if rotatory:
            fh = logging.handlers.RotatingFileHandler(logdir + LOGFILE_NAME,
                                                      maxBytes=MAX_LOGSIZE,
                                                      backupCount=MAX_LOGFILES)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


if __name__ == "__main__":

    # create my custom logger
    logger = get_logger(True, True, rotatory=True)

    # application code
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')
