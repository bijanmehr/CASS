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

def turnON():
    arduino_client('5')

def turnOFF():
    arduino_client('6')

def intro():
    arduino_client('3')

def outro():
    arduino_client('4')


def auto_mode():
    
    turnOFF()
    time.sleep(0.1)
    turnON()
    threading.Timer(60, turnOFF).start()
    threading.Timer(80, turnON).start()
    threading.Timer(140, turnOFF).start()
    threading.Timer(160, turnON).start()
    threading.Timer(220, turnOFF).start()



def lightwheel(data):
    print(data.data)
    if data.data == 'True':
        # turn lightwheel on
        turnON()
        print("ON")

    elif data.data == 'auto':
        # lightwheel patern
        auto_mode()
        print("auto")

    elif data.data == 'False':
        # turn lightwheel off
        turnOFF()
        print("OFF")

def curtain_handler(data):
    if(data.data == "start_parrot"):
        intro()
    elif(data.data == "stop_test"):
        outro()

def ros_init():
    rospy.init_node('arduino')
    rospy.Subscriber('web/stage', String, curtain_handler)
    rospy.Subscriber('web/wheel_status', String, lightwheel)
    rospy.spin()


if __name__ == "__main__":
        ros_init()
