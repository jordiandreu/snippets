import argparse
__author__='jandreu'

parser = argparse.ArgumentParser(description='demo script')
parser.add_argument('-d', '--device', help='device name or alias',
                    required=True)
parser.add_argument('-e', '--encoding', help='encoding type',
                    required=True)

args = parser.parse_args()

# show values
print 'Device name: %s' % args.device
print 'Encoding: %s' % args.encoding

