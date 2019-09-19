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
end_process = True
stage = ''

def set_action(msg):
    global current_frame1,current_frame2
    try:
        print(msg)
        action = msg.data
        with open(dir + '/logger.csv', 'a') as log_file :  
            log_file.write('%s,%d,%d,%s\n'%(stage,current_frame1,current_frame2,action))
          
    except CvBridgeError as e:
        print(e)



def seq1_callback(data):
    global first_seq1,current_frame1,end_process
    if end_process == False:
        if first_seq1 == -1:
            first_seq1 = data.header.seq
        else:
            current_frame1 = data.header.seq - first_seq1
    else:
        first_seq1 = -1
        current_frame1 = 0


def seq2_callback(data):
    global first_seq2,current_frame2,end_process
    if end_process == False:
        if first_seq2 == -1:
            first_seq2 = data.header.seq
        else:
            current_frame2 = data.header.seq - first_seq2
    else:
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
        # if cam1_subprocess is None:
        #     print('Start recording cam1')
        #     # filename_cam1 = "_filename:=\"%s/%s_cam1.avi\""%(dir,name)
        #     filename_cam1 = "\"%s/%s_cam1.avi\""%(dir,name)
        #     cmd1 = "roslaunch cabinet cam1_recorder.launch filename_cam1:=%s" %(filename_cam1)
        #     cam1_subprocess = subprocess.Popen(cmd1,shell=True)
        #     # cam1_subprocess = subprocess.Popen(["rosrun", "image_view","video_recorder",
        #     #     "image:=/camera1/image_raw",filename_cam1,"_fps:=30"],shell=True)
        
        # if cam2_subprocess is None:
        #     print('Start recording cam2')
        #     # filename_cam2 = "_filename:=\"%s/%s_cam2.avi\""%(dir,name)
        #     filename_cam2 = "\"%s/%s_cam2.avi\""%(dir,name)
        #     cmd2 = "roslaunch cabinet cam1_recorder.launch filename_cam2:=%s" %(filename_cam2)
        #     cam2_subprocess = subprocess.Popen(cmd2,shell=True)
        #     # cam2_subprocess = subprocess.Popen(["rosrun", "image_view","video_recorder",
        #     #     "image:=/camera2/image_raw",filename_cam2,"_fps:=30"],shell=True)

        if cam1_subprocess is None and cam2_subprocess is None:
            print("start recording")
            filename_cam1 = "\"%s/%s_cam1.avi\""%(dir,name)
            filename_cam2 = "\"%s/%s_cam2.avi\""%(dir,name)
            cmd = "roslaunch cabinet camera_recorder.launch filename_cam1:=%s filename_cam2:=%s" %(filename_cam1,filename_cam2)
            cam_subprocess = subprocess.Popen(cmd,shell=True)

def turn_off_cams():
    global cam1_subprocess,cam2_subprocess,cam_subprocess
    # if cam1_subprocess is not None:
    #     print('Stop recording')
    #     cam1_subprocess.terminate()
    #     cam1_subprocess = None

    # if cam2_subprocess is not None:
    #     print('Stop recording')
    #     cam2_subprocess.terminate()
    #     cam2_subprocess = None
    if cam_subprocess is not None:
        print("stop recording")
        # cam_subprocess.terminate()
        os.system("rosnode kill /cam1_recorder /cam2_recorder")
        # os.killpg(os.getpgid(cam_subprocess.pid), signal.SIGTERM)
        # os.killpg(os.getpgid(cam_subprocess.pid), signal.SIGTERM)


def start_end_logging(data):
    global end_process,stage
    if data.data == 'start_test':
        #begin recording on test stage
        stage = 'start_test'
        turn_on_cams('start_test')
        end_process = False

    elif data.data == 'start_wheel':
        #begin recording on wheel stage
        stage = 'start_wheel'
        turn_on_cams('start_wheel')
        end_process = False

    elif data.data == 'start_parrot':
        #begin recording on parrot stage
        stage = 'start_parrot'
        turn_on_cams('start_parrot')
        end_process = False

    elif data.data == 'stop_test':
        os.system("rosnode kill /cam1_recorder /cam2_recorder")

    else:
        #terminate recording
        turn_off_cams()
        end_process = True


def main():
    global data_writer

    rospy.init_node('cam_logger')
    # Define your image topic
    
    rospy.Subscriber('web/parrot_command', String, set_action)

    rospy.Subscriber("/camera1/camera_info", CameraInfo, seq1_callback)
    rospy.Subscriber("/camera2/camera_info", CameraInfo, seq2_callback)

    rospy.Subscriber("web/stage", String, start_end_logging)

    rospy.Subscriber('web/dir', String, set_dir)


    # Spin until ctrl + c
    rospy.spin()


if __name__ == '__main__':
    main()
