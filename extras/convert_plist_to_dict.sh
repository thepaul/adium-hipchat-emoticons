#!/bin/sh

xsltproc plist2xml.xsl ../Hipchat.AdiumEmoticonSet/Emoticons.plist | xsltproc transform.xsl -
