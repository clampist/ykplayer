#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import urllib2

flv = 'http://www.flvcd.com/parse.php?kw='

def fcd(flv, add, op):
    url = flv+add+op
    for line in urllib2.urlopen(url):
        if '" target="_blank" ' in line:
            st = line.split('"')[1]
            pl.write(st+'\n')

if __name__ == '__main__':
    pl = open('/tmp/plist', 'w')
    if sys.argv[1] == sys.argv[-1]:
        fcd(flv, sys.argv[-1], op='&format=normal')
    if sys.argv[1] == '-h':
        fcd(flv, sys.argv[-1], op='&format=high')
    if sys.argv[1] == '-s':
        fcd(flv, sys.argv[-1], op='&format=super')
    pl.close()
    os.system('mplayer -playlist /tmp/plist')
