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
    arduino_client('1')

def outro():
    arduino_client('2')


t1=threading.Timer(60, turnOFF)
t2=threading.Timer(80, turnON)
t3=threading.Timer(140, turnOFF)
t4=threading.Timer(160, turnON)
t5=threading.Timer(220, turnOFF)

def auto_mode():
    
    global t1,t2,t3,t4,t5
    turnOFF()
    time.sleep(0.1)
    turnON()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()



def lightwheel(data):
    global t1,t2,t3,t4,t5
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
        t1.cancel()
        t2.cancel()
        t3.cancel()
        t4.cancel()
        t5.cancel()

def curtain_handler(data):
    global t1,t2,t3,t4,t5
    if(data.data == "start_parrot"):
        intro()
        threading.Timer(0.1, turnOFF).start()
        t1.cancel()
        t2.cancel()
        t3.cancel()
        t4.cancel()
        t5.cancel()
    elif(data.data == "stop_test"):
        outro()

def ros_init():
    rospy.init_node('arduino')
    rospy.Subscriber('web/stage', String, curtain_handler)
    rospy.Subscriber('web/wheel_status', String, lightwheel)
    rospy.spin()


if __name__ == "__main__":
        ros_init()
