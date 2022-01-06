#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import rospy
from std_msgs.msg import Int32MultiArray as intarr
from glob import glob
from io import BytesIO
reload(sys)  
sys.setdefaultencoding('utf8')

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

back_cnt = 0
seq_cnt = 0
pre_seq_cnt = 0 
arr_cnt = 0
dist_cnt = 0

def int_callback(data):
    global back_cnt
    global seq_cnt
    global arr_cnt
    global pre_seq_cnt
    global dist_cnt
    seq = data.data[0]
    back = data.data[1]
    dist = data.data[2]
    lr = data.data[3]
    voice = "" 

    if lr == 0:
        ori_str = "왼쪽"
    if lr == 1:
        ori_str = "오른쪽"

    dist_str = str(dist) 
    if seq == 1000 :
        arr = 1
        arr_cnt = arr_cnt + arr
        if arr_cnt == 5:
            arr_cnt = 0
            voice = "  목적지에   도착하였습니다"
    elif seq == 0:
        voice = "  경로설정   중입니다    잠시만   기다려   주세요"
    elif back == 1:
        back_cnt = back_cnt + back
        if back_cnt == 5:
            back_cnt = 0
            voice = "  반대방향을   향하는   중입니다."
    elif (dist == 2 and dist != dist_cnt):
        if lr!=2:
            voice = "  다음   모퉁이에서   " + ori_str + "   방향으로    조심히   돌아주세요"
    elif seq_cnt != pre_seq_cnt and seq_cnt == seq and dist>5:
        if lr!=2:
            voice = "  " + dist_str + " 미터   앞에서    " + ori_str + "   방향으로   돌아주세요"
        else:
            voice = "  " + dist_str + "   미터   앞으로   진행해   주세요"

    elif dist%5 == 0 and dist != 0 and dist != dist_cnt:
        dist_str = str(dist) 
        voice = dist_str + "   미터 앞으로 진행해 주세요    "
    
    dist_cnt = dist
    pre_seq_cnt = seq_cnt
    seq_cnt = seq

    if voice:
        tts = gTTS( text=voice, lang='ko', slow=False ) 
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        song = AudioSegment.from_file(fp,format="mp3")
        play(song)

        fileList=glob("./ffcache*")
        for filePath in fileList:
            os.remove(filePath)

def voice(): 
    rospy.init_node('feedback')
    rospy.Subscriber('instruct',intarr,int_callback,queue_size =1)
    rospy.spin()
    
if __name__=='__main__':
    tts = gTTS( text='  안녕하세요 ', lang='ko', slow=False ) 
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    song = AudioSegment.from_file(fp,format="mp3")
    play(song)

    tts = gTTS( text=' 현재 과학기술관 3층 입니다.', lang='ko', slow=False) 
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    song = AudioSegment.from_file(fp,format="mp3")
    play(song)

    tts = gTTS( text=' 원하시는 목적지를 선택해 주세요  ', lang='ko', slow=False) 
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    song = AudioSegment.from_file(fp,format="mp3")
    play(song)

    try:
        voice()
    except rospy.ROSInterruptException:
        pass
