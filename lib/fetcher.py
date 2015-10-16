import urllib
import json
import logging

try:
    from ghost import Ghost
    ghost_available = True
except ImportError:
    ghost_available = False

HIPCHAT_URL = 'https://hipchat.com/'

def fetch_emoticons(options):
    if options.user and options.password:
        print 'using the webkit fetcher...'
        if ghost_available:
            return fetch_emoticons_ghost(options.user, options.password)
        else:
            print 'falling back to github (JSON) fetcher, since Ghost is not available...'

    print 'using JSON source from %s' % options.url
    params = urllib.urlencode({
        "max-results": options.max,
        "auth_token": options.token,
        "type": options.type
    })
    return fetch_emoticons_json("{0}?{1}".format(options.url, params))

def fetch_emoticons_ghost(username, password):
    ghost = Ghost()

    login(ghost, username, password)
    emoticons = dom_extract(ghost)

    return emoticons

def fetch_emoticons_json(json_url):
    stream = urllib.urlopen(json_url)
    emoticons = json.loads(stream.read())

    return emoticons

def login(ghost, username, password):
    ghost.open(HIPCHAT_URL + 'sign_in')
    ghost.fill('form', {
        'email': username,
        'password': password
        })

    ghost.click('#signin')
    ghost.wait_for_selector('a.action_icon.web')

def dom_extract(ghost):
    ghost.open(HIPCHAT_URL + 'chat')
    ghost.wait_for_selector('#status_ui')
    ghost.wait_for(lambda: ghost.evaluate('emoticons.emoticons.length > 27')[0], 'foo')
    emoticons, resources = ghost.evaluate('emoticons.emoticons')

    return emoticons
