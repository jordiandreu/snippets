import argparse
import ConfigParser
import os
# Use the argparse to get the config filename
# Use he filename to parse the config file


if __name__ == "__main__":

    desc = 'This is the description.'
    epil = 'This is the epilog.'

    ch = ['a', 'b', 'c']

    parser = argparse.ArgumentParser(description=desc, epilog=epil)
    parser.add_argument('config', metavar='configfile', type=str,
                        help='config filename')
    parser.add_argument('--only', type=str, nargs='+', choices=ch, help='help')

    args = parser.parse_args()

    if os.path.isfile(args.config):

        config=ConfigParser.SafeConfigParser()
        config.read(args.config) # config file name value
        name = config.get('author','name')
        surname = config.get('author','surname')
        print 'Hi, %s %s!' % (name, surname)
        fullname = config.get('author', 'fullname')
        print 'Officially: %s' % fullname

        name_list = config.items('author')
        for (x,y) in name_list:
            print 'x: %s, y: %s' % (x, y)
    else:
        print 'Config file %s does not exist.' % args.config
