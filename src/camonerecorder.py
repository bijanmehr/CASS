#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String
from sensor_msgs.msg import CameraInfo

bridge = CvBridge()
record_status = False

def main():
    rospy.init_node('CamOneRecorder')
    rospy.Subscriber('web/stage', String, set_stage)
    rospy.Subscriber('web/dir', String, set_dir)
    rospy.Subscriber("/camera1/image_raw", Image, image_callback)

def set_stage():
    global stage
    param = data.data
    if param == 'start_test':
        record_status = True
        writer_flag = True
        stage = 'stageONE'
    elif param == 'end_stage_one':
        record_status = False
    elif param == 'start_wheel':
        record_status = True
        writer_flag = True
        stage = 'stageTWO'
    elif param == 'end_stage_two':
        record_status = False
    elif param == 'start_parrot':
        record_status = True
        writer_flag = True
        stage = 'stageTHREE'
    elif param == 'end_test':
        record_status = False
    else:
        record_status = False
    return record_status,writer_flag

def set_dir():
    dir = data.data
    return dir

def image_callback():
    global data_writer,writer_flag
    try:
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        cv2_img = cv2.flip(cv2_img,1)

        if record_status == True:
            if writer_flag == True :
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                address = dir + '/camera1_%s.avi'%(stage)
                rospy.loginfo(address)
                data_writer = cv2.VideoWriter(address,fourcc, 30.0, (640,480))
                writer_flag = False


            try:
                data_writer.write(cv2_img)
            except Exception as e:
                print e

        elif record_status == False :
            try :
                data_writer.release()
            except Exception as e :
                print e


        # Save your OpenCV2 image as a jpeg
        cv2.imshow('camera_ONE_image', cv2_img)

        key = cv2.waitKey(1)

    except CvBridgeError, e:
        print(e)