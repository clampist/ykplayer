#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# +-----------------------------------------------------------------------------
# | File: ykplayer.py
# | Author: clampist
# | E-mail: clampist[at]gmail[dot]com
# | Last modified: 2012-10-23
# | Description:
# |     Linux 下优酷视频边下边播脚本，支持普清、高清、超清，能保留缓冲的视频文件
# | Copyrgiht (c) 2012 by clampist. All rights reserved.
# | License: GPLv3
# +-----------------------------------------------------------------------------

import os
import sys
import urllib2
import threading
from time import sleep

# 解决编码问题，中文无乱码
reload(sys)
sys.setdefaultencoding('utf-8')

# 需要下载的视频文件的地址列表
dlist = []
# 视频标题，用来作为保存文件名
title = []

flv = 'http://www.flvcd.com/parse.php?kw='

def fcd(flv, url, level):
    '''利用 flvcd 这个网站解析出真实视频地址'''
    downaddress = flv + url + level
    for line in urllib2.urlopen(downaddress):
        if '" target="_blank" ' in line:
            durl = line.split('"')[1]
            dlist.append(durl)
        if 'document.title' in line:
            title.append(line.decode('gb2312').split('"')[1])
            #print title[0]

def main(tag, fext):
    '''实现边下边播，优酷一般将视频7分钟分为一段，对小于7分钟和大于7分钟的分别处理'''
    #设置保存视频缓冲的路径
    path1 = os.environ['HOME']+'/videos/'
    if not os.path.isdir(path1):
        os.makedirs(path1)
    player = 'mplayer'

    #小于7分钟的视频
    if len(dlist) == 1:
        addr1 = path1 + title[0] + '_' + tag + fext
        cmmd = "wget "+dlist[0]+" -U 'Mozilla/5.0 (X11; Linux x86_64; rv:9.0.2) Gecko/20100101 Firefox/9.0.2' -O " + addr1
        #进程1下载
        def thread1():
            os.system(cmmd)

        play = player + ' ' + addr1
        #针对不同清晰度的视频缓冲不同的时间
        def thread2():
        #进程2播放
            if tag == 's':
                sleep(4)
            if tag == 'h':
                sleep(2)
            if tag == 'n':
                sleep(1)
            os.system(play)

    #大于7分钟的视频
    if len(dlist) > 1:
        #进程1下载
        def thread1():
            i = 0
            localpath1 = []
            cmmd = ''
            #print len(dlist)
            while(i < len(dlist)):
                i += 1
                filepath = path1 + title[0] + '_' + tag + str(i) + fext
                #保存到的本地文件列表
                localpath1.append(filepath)
                cmmd = "wget " + dlist[i-1] + " -U 'Mozilla/5.0 (X11; Linux x86_64; rv:6.0.2) Gecko/20100101 Firefox/6.0.2' -O " + localpath1[i-1]
                os.system(cmmd)

        #进程2播放
        def thread2():
            i = 0
            localpath2 = []
            #使用播放列表播放
            pl = open(path1 + title[0] + '_' + tag + '.li', 'w')
            if tag == 's':
                sleep(4)
            if tag == 'h':
                sleep(2)
            if tag == 'n':
                sleep(1)
            while(i < len(dlist)):
                i += 1
                filepath = path1 + title[0] + '_' + tag + str(i) + fext
                localpath2.append(filepath)
            for line in localpath2:
                pl.write(line+'\n')
            pl.close()
            play = player + ' -playlist ' + path1 + title[0] + '_' + tag + '.li'
            os.system(play)
    #多进程建立
    t1 = threading.Thread(target=thread1)
    t2 = threading.Thread(target=thread2)
    #多进程开始运行
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    try:
        #不同清晰度的视频，其文件类型分别保存
        if sys.argv[1] == sys.argv[-1]:
            fcd(flv, sys.argv[-1], level='&format=normal')
            main(tag='n', fext='.flv')
        if sys.argv[1] == '-h':
            fcd(flv, sys.argv[-1], level='&format=high')
            main(tag='h', fext='.mp4')
        if sys.argv[1] == '-s':
            fcd(flv, sys.argv[-1], level='&format=super')
            main(tag='s', fext='.flv')
    except IndexError:
        print '''Usage:
        python2 ykplayer.py [option] video_url
        option: -s 超清
                -h 高清
                -n 普清
        示例：python2 ykplayer.py -s http://v.youku.com/v_show/id_XNDU2MTUwNTQw.html'''

