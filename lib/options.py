from optparse import OptionParser

usage = "usage: %prog [options]"

parser = OptionParser(usage=usage)
parser.add_option('-u', '--user',
        action='store', type='string', dest='user',
        help='HipChat username to be used')
parser.add_option('-p', '--pass',
        action='store', type='string', dest='password',
        help='password to be used')

(options, args) = parser.parse_args()

if not (options.user and options.password):
    parser.error('username and password required!')
