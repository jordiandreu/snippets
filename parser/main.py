# coding=utf-8
#!/usr/bin/env python

import argparse
import ConfigParser

if __name__ == "__main__":

    description = 'Main script to show how a config parser works.'
    epilog = 'This is the end'

    parser = argparse.ArgumentParser(description=description,
                                     epilog=epilog)
    parser.add_argument('config', type=str, help='Config file')
    args = parser.parse_args()

    config = ConfigParser.RawConfigParser()
    config.read(args.config)
    catala_01 = config.get('Catala', 'var01')
    catala_02 = config.get('Catala', 'var02')
    english_01 = config.get('English', 'var01')
    english_02 = config.get('English', 'var02')

    print '%s/%s, %s/%s' % (catala_01, catala_02, english_01, english_02)

    for word, value in config.items('Catala'):
        print "En Catala %s es %s" % (word, value)


