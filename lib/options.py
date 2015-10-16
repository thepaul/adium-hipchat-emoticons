from optparse import OptionParser
from getpass import getpass

ROOT_URL="https://api.hipchat.com/v2/emoticon"
usage = "usage: %prog [options]"

parser = OptionParser(usage=usage)
parser.add_option('-u', '--user',
        help='HipChat username to be used')
parser.add_option('-t', '--token',
        help='Hipchat Auth Token')
parser.add_option('-y', '--type',
        choices=['global', 'group', 'all'], default='global',
        help='specify which emoticons to get')
parser.add_option('-m', '--max',
        type=int, default=1000,
        help='specify the max number of emoticons to return')
parser.add_option('-f', '--url',
        default=ROOT_URL,
        help='specify location of JSON input (default: %s)' % ROOT_URL)

(options, args) = parser.parse_args()

if options.user:
    password = getpass()
    setattr(options, 'password', password)
