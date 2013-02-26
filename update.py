#!/usr/bin/python
import os

from lib import build_bundle
from lib import fetch_emoticons
from lib import options

root_dir = os.path.dirname(__file__)

emoticons = fetch_emoticons(options.user, options.password)
build_bundle(emoticons, root_dir)
