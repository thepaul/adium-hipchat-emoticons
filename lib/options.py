from optparse import OptionParser

DEFAULT_JSON_LOCATION = 'https://github.com/henrik/hipchat-emoticons/master/emoticons.json'

usage = "usage: %prog [options]"

parser = OptionParser(usage=usage)
parser.add_option('-u', '--user',
        action='store', type='string', dest='user',
        help='HipChat username to be used')
parser.add_option('-p', '--pass',
        action='store', type='string', dest='password',
        help='password to be used')
parser.add_option('-f', '--url',
        action='store', type='string', dest='url', default=DEFAULT_JSON_LOCATION,
        help='specify location of JSON input (default: %s)' % DEFAULT_JSON_LOCATION)

(options, args) = parser.parse_args()
