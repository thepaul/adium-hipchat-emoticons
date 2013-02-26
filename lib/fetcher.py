from ghost import Ghost
import time

HIPCHAT_URL = 'https://hipchat.com/'

def login(ghost, username, password):
    ghost.open(HIPCHAT_URL + 'sign_in')
    #time.sleep(2)
    ghost.fill('form', {
        'email': username,
        'password': password
        })

    ghost.click('#signin')
    ghost.wait_for_selector('a.action_icon.web')

def extract_emoticons(ghost):
    ghost.open(HIPCHAT_URL + 'chat')
    ghost.wait_for_selector('#status_ui')
    ghost.wait_for(lambda: ghost.evaluate('emoticons.emoticons.length > 27')[0], 'foo')
    emoticons, resources = ghost.evaluate('emoticons.emoticons')

    return emoticons

def fetch_emoticons(username, password):
    ghost = Ghost(wait_timeout=20)

    login(ghost, username, password)
    emoticons = extract_emoticons(ghost)

    return emoticons
