#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String
from sensor_msgs.msg import CameraInfo

import cv2
import time
import os
from os.path import expanduser
import datetime

bridge = CvBridge()


# def image_callback(msg):
#     # global data_writer
#     try:
#         cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
#         cv2_img = cv2.flip(cv2_img,1)

#         fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#         address = '/home/bmh/Desktop/camera1.avi'
#         data_writer = cv2.VideoWriter(address,fourcc, 30.0, (640,480))

#         try:
#             data_writer.write(cv2_img)
#         except Exception as e:
#             print e

        
#         key = cv2.waitKey(1)
#         # print "key pressed: " + str(key)
#         if key == 27:
#             try :
#                 data_writer.release()
#             except Exception as e :
#                 print e
#         cv2.imshow('camera_image', cv2_img)
#     except CvBridgeError, e:
#         print(e)

end_process = False
writer_flag = True

def image_callback(msg):
    global data_writer,writer_flag
    try:
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        cv2_img = cv2.flip(cv2_img,1)
        if writer_flag == True :
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            address = '/home/bmh/Desktop/camera1.avi'
            # rospy.loginfo(address)
            data_writer = cv2.VideoWriter(address,fourcc, 30.0, (640,480))
            writer_flag = False

        try:
            data_writer.write(cv2_img)
        except Exception as e:
            print e


        # Save your OpenCV2 image as a jpeg
        cv2.imshow('camera_image1', cv2_img)

        key = cv2.waitKey(1)

    except CvBridgeError, e:
        print(e)


def main():
    rospy.init_node('camera_listener')
    image_topic = "/usb_cam/image_raw"
    rospy.Subscriber(image_topic, Image, image_callback)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
