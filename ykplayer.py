#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import urllib2
import threading
from time import sleep

reload(sys)
sys.setdefaultencoding('utf-8')

dlist = []
title = []

flv = 'http://www.flvcd.com/parse.php?kw='

def fcd(flv, add, op):
    url = flv+add+op
    for line in urllib2.urlopen(url):
        if '" target="_blank" ' in line:
            st = line.split('"')[1]
            dlist.append(st)
        if 'document.title' in line:
            title.append(line.decode('gb2312').split('"')[1])
#            print title[0]

def main(tag, fext):
    if len(dlist) == 1:
        a1 = '/home/clampist/videos/'+title[0]+'_'+tag+fext
        cmmd = "wget "+dlist[0]+" -U 'Mozilla/5.0 (X11; Linux x86_64; rv:9.0.2) Gecko/20100101 Firefox/9.0.2' -O " + a1

        def thread1():
            os.system(cmmd)
        play = 'mplayer ' + a1
        def thread2():
            if tag == 's':
                sleep(4)
            if tag == 'h':
                sleep(2)
            if tag == 'n':
                sleep(1)
            os.system(play)

    if len(dlist) > 1:
        def thread1():
            i = 0
            dl1 = []
            cmmd = ''
            print len(dlist)
            while(i < len(dlist)):
                i += 1
                st = '/home/clampist/videos/'+title[0]+'_'+tag+str(i)+fext
                dl1.append(st)
                cmmd = "wget "+dlist[i-1]+" -U 'Mozilla/5.0 (X11; Linux x86_64; rv:6.0.2) Gecko/20100101 Firefox/6.0.2' -O " + dl1[i-1]
                os.system(cmmd)

        def thread2():
            i = 0
            dl2 = []
            pl = open('/home/clampist/videos/'+title[0]+'_'+tag+'.li', 'w')
            if tag == 's':
                sleep(4)
            if tag == 'h':
                sleep(2)
            if tag == 'n':
                sleep(1)
            while(i < len(dlist)):
                i += 1
                st = '/home/clampist/videos/'+title[0]+'_'+tag+str(i)+fext
                dl2.append(st)
            for line in dl2:
                pl.write(line+'\n')
            pl.close()
            play = 'mplayer -playlist ' + '/home/clampist/videos/'+title[0]+'_'+tag+'.li'
            os.system(play)

    t1 = threading.Thread(target=thread1)
    t2 = threading.Thread(target=thread2)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    if sys.argv[1] == sys.argv[-1]:
        fcd(flv, sys.argv[-1], op='&format=normal')
        main(tag='n', fext='.flv')
    if sys.argv[1] == '-h':
        fcd(flv, sys.argv[-1], op='&format=high')
        main(tag='h', fext='.mp4')
    if sys.argv[1] == '-s':
        fcd(flv, sys.argv[-1], op='&format=super')
        main(tag='s', fext='.flv')
