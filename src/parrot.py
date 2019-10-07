#!/usr/bin/env python
import rospy
import serial
import time
import threading
from cabinet.srv import *
from std_msgs.msg import String
from timeloop import Timeloop
from datetime import timedelta
from timeit import default_timer as timer

auto_flag = False


def parrot_queue_handler():
    global parrot_funcs , parrot_funcs_params ,parrot_funcs_delay
    try:
        if parrot_funcs:
            rospy.logerr(parrot_funcs)
            if parrot_funcs_delay[0] != -1:
                time.sleep(parrot_funcs_delay[0])

            if parrot_funcs_params[0] != -1:
                parrot_funcs[0](parrot_funcs_params[0])
            else:
                parrot_funcs[0]()

            parrot_funcs.pop(0)
            parrot_funcs_params.pop(0)
            parrot_funcs_delay.pop(0)

    except Exception as e :
        rospy.logerr('error in parrot_queue_handler ! : %s'%e)
        # print('error in parrot_queue_handler !',e)


    t = threading.Timer(0.1, parrot_queue_handler)
    t.daemon = True
    t.start()




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
    if(res.find("DONE") != 1):
        print ("done")
    else:
        print("not done")

def blink(pwm = 180):
    res = parrot_client('G2 S%d'%pwm)
    if(res.find("DONE") != 1):
        print ("done")
    else:
        print("not done")

def mouth(pwm = 0): # open and close the mouth 255 -> open mouth      0 -> close mouth
    res = parrot_client('G3 S%d'%pwm)
    if(res.find("DONE") != 1):
        print ("done")
    else:
        print("not done")

def open_eye(pwm = 130):
    res = parrot_client('G4 S%d'%pwm)
    if(res.find("DONE") != 1):
        print ("done")
    else:
        print("not done")

def close_eye(pwm = 105):
    res = parrot_client('G5 S%d'%pwm)
    if(res.find("DONE") != 1):
        print ("done")
    else:
        print("not done")

def toggle():
    global auto_flag
    auto_flag = not(auto_flag)

def talk():
    pop_all_parrot_funcs()
    append_to_parrot_funcs(mouth,240)
    append_to_parrot_funcs(mouth,0,0.5)
    append_to_parrot_funcs(mouth,240,0.5)
    append_to_parrot_funcs(mouth,0,0.5)





parrot_funcs = []
parrot_funcs_params = []
parrot_funcs_delay = []

def append_to_parrot_funcs(functions,param = -1,delay = -1):
    global parrot_funcs , parrot_funcs_params ,parrot_funcs_delay
    parrot_funcs.append(functions)
    parrot_funcs_params.append(param)
    parrot_funcs_delay.append(delay)

def pop_all_parrot_funcs():
    global parrot_funcs , parrot_funcs_params ,parrot_funcs_delay
    parrot_funcs = []
    parrot_funcs_params = []
    parrot_funcs_delay = []



def parrot_commands(data):
    if(int(data.data) == 0 ):   # dance
        append_to_parrot_funcs(dance)
    elif(int(data.data) == 1 ):  # blink
        append_to_parrot_funcs(blink)
    elif(int(data.data) == 2 ): # open mouth
        append_to_parrot_funcs(mouth,240)
    elif(int(data.data) == 3 ): # close mouth
        append_to_parrot_funcs(mouth,0)
    elif(int(data.data) == 4 ): # open eye
        append_to_parrot_funcs(open_eye)
    elif(int(data.data) == 5 ): # close eye
        append_to_parrot_funcs(close_eye)
    elif(int(data.data) == 6): # open and close mouth
        append_to_parrot_funcs(mouth,240)
        append_to_parrot_funcs(mouth,0,0.5)
        append_to_parrot_funcs(mouth,240,0.5)
        append_to_parrot_funcs(mouth,0,0.5)



def auto_dance():
    if auto_flag:
        append_to_parrot_funcs(dance)

    t = threading.Timer(7, auto_dance)
    t.daemon = True
    t.start()


def auto_blink():
    if auto_flag:
        append_to_parrot_funcs(blink)

    t = threading.Timer(3, auto_blink)
    t.daemon = True
    t.start()


def auto_talk():
    if auto_flag:
        append_to_parrot_funcs(talk)

    t = threading.Timer(5, auto_talk)
    t.daemon = True
    t.start()


# TODO chk auto
def auto_mode():
    pass
    # if(auto_flag == True):
    #     tl.start(block=True)
    # elif(auto_flag == False):
    #     tl.stop()
    
# TODO implement in parrot auto_mode
def stop_function(data):
    global auto_flag
    if data.data == 'stop_test':
        auto_flag = False

def auto(data):
    global auto_flag
    if(data.data =="auto"):
        auto_flag = True
    elif(data.data == "manual"):
        auto_flag = False
    
def parrot_voice_commands(data):
    global auto_flag
    text = data.data
    if text.find("shutup") == -1:
        auto_flag = False
        talk()
        # auto_flag = True
        threading.Timer(0.5, toggle)

# def auto_step(data):
#     global auto_flag
#     auto_flag = False
#     talk()
#     threading.Timer(0.5, toggle)

def ros_init():
    rospy.init_node('parrot', log_level=rospy.DEBUG)
    rospy.Subscriber('web/parrot_commands', String, parrot_commands, queue_size=10)
    rospy.Subscriber('web/parrot_command_type', String, auto, queue_size=10)
    rospy.Subscriber("web/parrot_voice_commands", String, parrot_voice_commands, queue_size=10)
    rospy.Subscriber("web/stage", String, stop_function)
    # rospy.Subscriber("auto_mode", String, auto_step)
    rospy.spin()


if __name__ == "__main__":
    parrot_queue_handler()
    auto_dance()
    auto_talk()
    auto_blink()
    ros_init()