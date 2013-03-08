import sys
import os
import json
import urllib
from xml.sax.saxutils import unescape
from StringIO import StringIO
from collections import namedtuple

hipchat_emoticons_github = 'https://github.com/henrik/hipchat-emoticons'
hipchat_emoticons_dl = 'https://dujrsrsgsd3nh.cloudfront.net/img/emoticons'

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

Emot = namedtuple('Emot', ('name', 'imgbase', 'imgpath', 'shortcuts'))

def merge_identical_emoticons(emoticons):
    emotedict = {}
    for emot in emoticons:
        imgname = os.path.basename(emot['image'])
        emotobj = emotedict.get(imgname)
        shortcut = unescape(emot['shortcut'])
        # special case, work around bug(?) in henrik code
        if shortcut == ':':
            shortcut = ':/'
        if emotobj is None:
            emotedict[imgname] = emotobj = Emot(shortcut, imgname, emot['image'], [])
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

def update_icon(imgpath, destfile):
    urllib.urlretrieve(hipchat_emoticons_dl + '/' + imgpath, destfile)

def update_bundle(bundle_path, emoticons):
    write_plist(os.path.join(bundle_path, 'Emoticons.plist'), emoticons)
    for emot in emoticons:
        update_icon(emot.imgpath, os.path.join(bundle_path, emot.imgbase))

def build_bundle(emoticons, root_dir):
    emoticons = merge_identical_emoticons(emoticons)
    adium_bundle = os.path.join(root_dir, 'Hipchat.AdiumEmoticonSet')
    update_bundle(adium_bundle, emoticons)
