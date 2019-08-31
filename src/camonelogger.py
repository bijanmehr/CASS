#!/usr/bin/env python

import rospy
import os
from datetime import datetime
import csv
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String
from sensor_msgs.msg import CameraInfo

def main():
    rospy.init_node('CameraOneLogger')
    rospy.Subscriber('web/stage', String, set_stages)
    rospy.Subscriber('web/dir', String, dir_handler)
    rospy.Subscriber('web/wheel_status ', String, lightwheel_status_log)
    rospy.Subscriber('web/parrot_command_name', String, parrot_action_logs)
    rospy.Subscriber("/camera1/camera_info", CameraInfo, seq_callback_cam1)

def stage():
    pass

def dir_handler():
    dir = os.path.expanduser(data.data)
    if not os.path.exists(dir):
        rospy.logwarn('directory is not exist!')
    else:
        return dir
        with open(dir + '/CameraOnelog.csv', 'a') as log_file :
            log_file.write('time, cam1_frame_num, action\n')
            rospy.loginfo('log file created!('+dir+'/log.csv)')

def lightwheel_status_log():
    pass

def parrot_action_logs():
    pass

def seq_callback_cam1():
    pass