#!/usr/bin/env python
import rospy
import serial
import time
import threading
from cabinet.srv import *
from std_msgs.msg import String



# play_sound = None
# stop_sound = None


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

def mouth(pwm): # open and close the mouth 255 -> open mouth      0 -> close mouth
    res = parrot_client('G3 S%d'%pwm)
    # if(res.find("DONE") != 1):
    #     print ("done")
    # else:
    #     print("not done")

def open_eye(pwm = 130):
    res = parrot_client('G4 S%d'%pwm)

def close_eye(pwm = 105):
    res = parrot_client('G5 S%d'%pwm)



def parrot_voice_commands(data):
    # TODO: frequency, test on parrot
    # play_sound.publish(data.data)
    mouth(240)
    time.sleep(0.3)
    mouth(0)
    time.sleep(0.3)
    mouth(240)
    time.sleep(0.3)
    mouth(0)

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
    elif(int(data.data) == 6 ): # close eye
        auto_mode(5,0.6)


# # TODO test auto mode
def auto_mode(num = 3,time_step = 0.5):
    i = 0
    while i <= num:
        blink()
        time.sleep(time_step)
        dance()
        time.sleep(time_step)
        i = i+1

def ros_init():
    rospy.init_node('parrot', log_level=rospy.DEBUG)
    # play_sound = rospy.Publisher('audio_player/play_sound', String, queue_size=10)
    # stop_sound = rospy.Publisher('audio_player/stop_sound', String, queue_size=10)
    rospy.Subscriber('web/parrot_commands', String, parrot_commands, queue_size=10)
    rospy.Subscriber("web/parrot_voice_commands", String, parrot_voice_commands, queue_size=10)
    rospy.spin()


if __name__ == "__main__":
        ros_init()