#!/usr/bin/env python

import rospy
from std_msgs.msg import String

from sensor_msgs.msg import CameraInfo

import time
import os
import signal
from os.path import expanduser
import datetime
import subprocess


writer_flag = False
first_seq1 = -1
current_frame1 = 0
first_seq2 = -1
current_frame2 = 0
cam1_subprocess = None
cam2_subprocess = None

cam_subprocess = None

dir = None
stage = ''


def log_parrot_wheel(msg):
    global current_frame1,current_frame2
    log_on_file('%s,%d,%d,%s\n'%(stage,current_frame1,current_frame2,msg.data))


def log_on_file(string):
    try:
        with open(dir + '/logger.csv', 'a') as log_file :  
            log_file.write(string)
          
    except Exception as e:
        print(e)


def seq1_callback(data):
    global first_seq1,current_frame1
    if first_seq1 == -1:
        first_seq1 = data.header.seq
    else:
        current_frame1 = data.header.seq - first_seq1



def seq2_callback(data):
    global first_seq2,current_frame2
    if first_seq2 == -1:
        first_seq2 = data.header.seq
    else:
        current_frame2 = data.header.seq - first_seq2


def reset_frame_number():
    global first_seq2,current_frame2,first_seq1,current_frame1
    first_seq1 = -1
    current_frame1 = 0
    first_seq2 = -1
    current_frame2 = 0


def set_dir(data):
    global dir,writer_flag
    dir = str(data.data)
    print dir
    writer_flag = True



def turn_on_cams(name):
    global cam1_subprocess,cam2_subprocess,dir,cam_subprocess

    if writer_flag == True:

        if cam1_subprocess is None and cam2_subprocess is None:
            print("start recording")
            filename_cam1 = "\"%s/%s_cam1.avi\""%(dir,name)
            filename_cam2 = "\"%s/%s_cam2.avi\""%(dir,name)
            cmd = "roslaunch cabinet camera_recorder.launch filename_cam1:=%s filename_cam2:=%s" %(filename_cam1,filename_cam2)
            cam_subprocess = subprocess.Popen(cmd,shell=True)

def turn_off_cams():
    global cam1_subprocess,cam2_subprocess,cam_subprocess

    if cam_subprocess is not None:
        print("stop recording")
        os.system("rosnode kill /cam1_recorder /cam2_recorder")
        cam1_subprocess = None
        cam2_subprocess = None



def start_end_logging(data):
    global stage


    if data.data == 'start_test':
        #begin recording on test stage
        stage = 'start_test'
        turn_on_cams('start_test')

    elif data.data == 'start_wheel':
        #begin recording on wheel stage
        stage = 'start_wheel'
        turn_on_cams('start_wheel')

    elif data.data == 'start_parrot':
        #begin recording on parrot stage
        stage = 'start_parrot'
        turn_on_cams('start_parrot')

    elif data.data == 'stop_test':
        os.system("rosnode kill /cam1_recorder /cam2_recorder")
        reset_frame_number()

    else:
        #terminate recording
        turn_off_cams()
        reset_frame_number()


def main():
    global data_writer

    rospy.init_node('cam_logger')
    # Define your image topic
    

    rospy.Subscriber('web/parrot_command_name', String, log_parrot_wheel)
    rospy.Subscriber('web/wheel_status', String, log_parrot_wheel)

    rospy.Subscriber("/camera1/camera_info", CameraInfo, seq1_callback)
    rospy.Subscriber("/camera2/camera_info", CameraInfo, seq2_callback)

    rospy.Subscriber("web/stage", String, start_end_logging)

    rospy.Subscriber('web/dir', String, set_dir)


    # Spin until ctrl + c
    rospy.spin()


if __name__ == '__main__':
    time.sleep(1)
    main()
