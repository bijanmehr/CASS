#!/usr/bin/env python
import rospy
import serial
import time
import threading
from cabinet.srv import *
from std_msgs.msg import String

from timeit import default_timer as timer

stop_flag = True
# time_auto_mode = 10

def parrot_client(command):
    rospy.wait_for_service('serial_handler/parrot')
    try:
        parrot_connection = rospy.ServiceProxy('serial_handler/parrot', parrot)
        result = parrot_connection(command)
        return result.result
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def dance(number = 1):
    res = parrot_client('G1 S%d'%number)
    # if(res.find("DONE") != 1):
    #     print ("done")
    # else:
    #     print("not done")

def blink(pwm = 180):
    res = parrot_client('G2 S%d'%pwm)
    # if(res.find("DONE") != 1):
    #     print ("done")
    # else:
    #     print("not done")

def mouth(pwm = 0): # open and close the mouth 255 -> open mouth      0 -> close mouth
    res = parrot_client('G3 S%d'%pwm)
    # if(res.find("DONE") != 1):
    #     print ("done")
    # else:
    #     print("not done")

def open_eye(pwm = 130):
    res = parrot_client('G4 S%d'%pwm)
    # if(res.find("DONE") != 1):
    #     print ("done")
    # else:
    #     print("not done")

def close_eye(pwm = 105):
    res = parrot_client('G5 S%d'%pwm)
    # if(res.find("DONE") != 1):
    #     print ("done")
    # else:
    #     print("not done")

def talk():
    mouth(240)
    threading.Timer(0.5, mouth, args=[0]).start()
    threading.Timer(1, mouth, args=[240]).start()
    threading.Timer(1.5, mouth, args=[0]).start()



def parrot_commands(data):
    if(int(data.data) == 0 ):   # dance
        dance()
    elif(int(data.data) == 1 ):  # blink
        blink()
    elif(int(data.data) == 2 ): # open mouth
        mouth(255)
    elif(int(data.data) == 3 ): # close mouth
        mouth(0)
    elif(int(data.data) == 4 ): # open eye
        open_eye()
    elif(int(data.data) == 5 ): # close eye
        close_eye()
    # elif(int(data.data) == 6): # open and close mouth
    #     mouth(240)
    #     threading.Timer(0.5, mouth, args=[0]).start()
    #     threading.Timer(1, mouth, args=[240]).start()
    #     threading.Timer(1.5, mouth, args=[0]).start()

# def toggle():
#     global auto_flag
#     auto_flag != auto_flag


# TODO chk auto
def auto_mode():
    
    threading.Timer(0.01, blink).start()
    threading.Timer(0.8, dance).start()

    threading.Timer(1.5, blink).start()
    threading.Timer(2.5, dance).start()

    threading.Timer(4, blink).start()
    threading.Timer(4.5, dance).start()

    threading.Timer(5.5, blink).start()
    threading.Timer(7.5, dance).start()

    threading.Timer(8, blink).start()
    threading.Timer(9.5, dance).start()

    threading.Timer(9.5, blink).start()
    threading.Timer(11.5, dance).start()

    threading.Timer(12, blink).start()
    threading.Timer(13.5, dance).start()

    threading.Timer(14, blink).start()
    threading.Timer(16.5, dance).start()
    
# TODO implement in parrot auto_mode
def stop_function(data):
    global stop_flag
    if data.data == 'stop_test':
        stop_flag = False

def auto(data):
    if(data.data == "auto"):
        auto_mode()

def parrot_voice_commands(data):
    text = data.data
    if text.find("shutup") == -1:
        talk()

def ros_init():
    rospy.init_node('parrot', log_level=rospy.DEBUG)
    rospy.Subscriber('web/parrot_commands', String, parrot_commands, queue_size=10)
    rospy.Subscriber('web/parrot_command_type', String, auto, queue_size=10)
    rospy.Subscriber("web/parrot_voice_commands", String, parrot_voice_commands, queue_size=10)
    rospy.Subscriber("web/stage", String, stop_function)
    rospy.spin()


if __name__ == "__main__":
        ros_init()