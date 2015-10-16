import sys
import os
import json
import urllib
from xml.sax.saxutils import unescape
from StringIO import StringIO
from collections import namedtuple


plist_header = '''\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>AdiumSetVersion</key>
    <real>1.3</real>
    <key>Emoticons</key>
    <dict>
'''

plist_footer = '''\
    </dict>
  </dict>
</plist>'''  # no eol- this is important

plist_item = '''\
        <key>%(imgbase)s</key>
      <dict>
        <key>Equivalents</key>
        <array>
          %(shortcuts)s
        </array>
        <key>Name</key>
        <string>%(name)s</string>
      </dict>
'''

default_emoticon_set = [
							['(thumbsup)', 'thumbs_up.png', '', ['(thumbsup)'] ],
							['(thumbsdown)', 'thumbs_down.png', '', ['(thumbsdown)'] ],
							['(embarrassed)', 'embarrassed.png', '', ['(embarrassed)'] ],
							['(oops)', 'oops.png', '', ['(oops)'] ],
							['8)', 'cool.png', '', ['8)', '8-)'] ],
							[':#', 'footinmouth.png', '', [':#'] ],
							[':$', 'moneymouth.png', '', [':$'] ],
							[':\'(', 'cry.png', '', [':\'('] ],
							[':(', 'frown.png', '', [':(', ':-('] ],
							[':)', 'smile.png', '', [':)', ':-)', '=)'] ],
							[':-*', 'kiss.png', '', [':-*'] ],
							[':D', 'bigsmile.png', '', [':D', ':-D'] ],
							[':Z', 'sealed.png', '', [':Z', ':-Z', ':z', ':-z'] ],
							[':\\', 'slant.png', '', [':\\', ':/'] ],
							[':o', 'gasp.png', '', [':o', ':-o'] ],
							[':p', 'tongue.png', '', [':p', ':-p', ':P', ':-P'] ],
							[':|', 'straightface.png', '', [':|', ':-|'] ],
							[';)', 'wink.png', '', [';)', ';-)'] ],
							[';p', 'winktongue.png', '', [';p', ';-p', ';P', ';-P'] ],
							['>:-(', 'angry.png', '', ['>:-('] ],
							['O:)', 'innocent.png', '', ['O:)', 'o:)'] ]
                       ]

Emot = namedtuple('Emot', ('name', 'imgbase', 'imgurl', 'shortcuts'))

def merge_identical_emoticons(emoticons):
    emotedict = {}
    for emot in emoticons['items']:
        imgname = os.path.basename(emot['url'])
        emotobj = emotedict.get(imgname)
        shortcut = '(' + unescape(emot['shortcut']) + ')'
        if emotobj is None:
            emotedict[imgname] = emotobj = Emot(shortcut, imgname, emot['url'], [])
        emotobj.shortcuts.append(shortcut)
    return sorted(emotedict.values())

def write_plist_key(f, emot):
    shortcuts = '\n          '.join(['<string>%s</string>' % (s,) for s in emot.shortcuts])
    f.write(plist_item % {'imgbase': emot.imgbase,
                          'shortcuts': shortcuts,
                          'name': emot.name})

def write_plist_stream(f, emoticons):
    f.write(plist_header)
    for emot in emoticons:
        write_plist_key(f, emot)      
    f.write(plist_footer)

def write_plist(plist_path, emoticons):
    with open(plist_path, 'w') as f:
        return write_plist_stream(f, emoticons)

def update_icon(imgurl, destfile):
    if not os.path.isfile(destfile) and imgurl != '':
       urllib.urlretrieve(imgurl, destfile)
       
def cleanup_bundle(bundle_path, emoticons):
    emot_files = [ 'Emoticons.plist' ]
    for emot in emoticons:
        emot_files.append(emot.imgbase)
    bundle_files = os.listdir(bundle_path)
    for bundle_file in bundle_files:
        bundle_file_full = os.path.join(bundle_path, bundle_file)
        if (not bundle_file in emot_files) and os.path.isfile(bundle_file_full):
            os.remove(bundle_file_full)
    

def update_bundle(bundle_path, emoticons):
    write_plist(os.path.join(bundle_path, 'Emoticons.plist'), emoticons)
    for emot in emoticons:
        update_icon(emot.imgurl, os.path.join(bundle_path, emot.imgbase))
    cleanup_bundle(bundle_path, emoticons)

def build_bundle(emoticons, root_dir):
    emoticons = merge_identical_emoticons(emoticons)
    adium_bundle = os.path.join(root_dir, 'Hipchat.AdiumEmoticonSet')
    for emot in default_emoticon_set:
        emotobj = Emot._make(emot)
        emoticons.append(emotobj)
    update_bundle(adium_bundle, emoticons)
