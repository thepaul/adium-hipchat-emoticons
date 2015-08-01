from optparse import OptionParser
from getpass import getpass

DEFAULT_JSON_LOCATION = 'https://api.hipchat.com/v2/emoticon?max-results=1000&type=global&auth_token='

usage = "usage: %prog [options]"

parser = OptionParser(usage=usage)
parser.add_option('-u', '--user',
        action='store', type='string', dest='user',
        help='HipChat username to be used')
parser.add_option('-f', '--url',
        action='store', type='string', dest='url', default=DEFAULT_JSON_LOCATION,
        help='specify location of JSON input (default: %s)' % DEFAULT_JSON_LOCATION)

(options, args) = parser.parse_args()

if options.user:
    password = getpass()
    setattr(options, 'password', password)
