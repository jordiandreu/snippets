import argparse
#https://docs.python.org/2/howto/argparse.html

description = 'calculate X to the power of Y'
epilog = 'This is the end'

parser = argparse.ArgumentParser(description=description,
                                 epilog=epilog)
ch = ['hex','oct']
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("-b", '--base', type=str, nargs='+', choices=ch, help='base type')
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
parser.add_argument("-a", '--add', nargs='+', help='add exponents')
args = parser.parse_args()
answer = args.x**args.y

print args.add

if args.base == ch[0]:
    answer = hex(answer)
    print 'f'
elif args.base == ch[1]:
    answer = oct(answer)

if args.quiet:
    print answer
elif args.verbose:
    print "{} to the power {} equals {}".format(args.x, args.y, answer)
else:
    print "{}^{} == {}".format(args.x, args.y, answer)