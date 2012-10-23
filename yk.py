#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# +-----------------------------------------------------------------------------
# | File: yk.py
# | Author: clampist
# | E-mail: clampist[at]gmail[dot]com
# | Last modified: 2012-10-23
# | Description:
# |     Linux 下优酷视频边下边播脚本，支持普清、高清、超清，ykplayer.py的简化版
# | Copyrgiht (c) 2012 by clampist. All rights reserved.
# | License: GPLv3
# +-----------------------------------------------------------------------------

import os
import sys
import urllib2

flv = 'http://www.flvcd.com/parse.php?kw='

def fcd(flv, url, level):
    '''利用 flvcd 这个网站解析出真实视频地址'''
    downaddress = flv + url + level
    for line in urllib2.urlopen(downaddress):
        if '" target="_blank" ' in line:
            st = line.split('"')[1]
            pl.write(st+'\n')

if __name__ == '__main__':
    #播放列表文件
    pl = open('/tmp/plist', 'w')
    try:
        if sys.argv[1] == sys.argv[-1]:
            fcd(flv, sys.argv[-1], level='&format=normal')
        if sys.argv[1] == '-h':
            fcd(flv, sys.argv[-1], level='&format=high')
        if sys.argv[1] == '-s':
            fcd(flv, sys.argv[-1], level='&format=super')
        pl.close()
        #mplayer 播放在线流视频
        os.system('mplayer -playlist /tmp/plist')
    except IndexError:
        print '''Usage:
        python2 yk.py [option] video_url
        option: -s 超清
                -h 高清
                -n 普清
        示例：python2 yk.py -s http://v.youku.com/v_show/id_XNDY0OTY2NDE2.html'''
