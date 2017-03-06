import argparse


def main():
    parser = argparse.ArgumentParser(description='demo script')
    parser.add_argument('-d', '--device', help='device name',
                        required=True)
    parser.add_argument('-e', '--encoding', help='encoding type',
                        required=True)

    args = parser.parse_args()

    print 'Device name: %s' % args.device
    print 'Encoding: %s' % args.encoding


if __name__ == '__main__':
    main()
