#!/usr/bin/env python
import rospy
import serial
import time
import threading
from cabinet.srv import *
from std_msgs.msg import String



def arduino_client(command):
    rospy.wait_for_service('serial_handler/arduino')
    try:
        arduino_connection = rospy.ServiceProxy('serial_handler/arduino', Arduino)
        result = arduino_connection(command)
        print(result)
        return result.result
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e





def arduino_commands(data):
    # print("get here")
    if(int(data.data) == 90 ):   # trun lightwheel on
        arduino_client('5')
    elif(int(data.data) == 91 ):  # trun lightwheel off
        arduino_client('6')
    elif(int(data.data) == 92 ):  # trun LED on and open curtain
        arduino_client('7')
    elif(int(data.data) == 93 ):  # trun LED off and close curtain
        arduino_client('8')


def ros_init():
    rospy.init_node('arduino')
    rospy.Subscriber('web/arduino_commands', String, arduino_commands)
    rospy.spin()


if __name__ == "__main__":
        ros_init()
