#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import pygame
import time
import threading
import math

sounds = ["/home/bmh/Desktop/cabinet_WebApp/media/1_salam-kocholo.wav"
    ,"/home/bmh/Desktop/cabinet_WebApp/media/2_khobi.wav"
    ,"/home/bmh/Desktop/cabinet_WebApp/media/3_esm-man-abi-e.wav"
    ,"/home/bmh/Desktop/cabinet_WebApp/media/4_bia-pish-man.wav"
    ,"/home/bmh/Desktop/cabinet_WebApp/media/5_mikham-barat-ahang-pakhsh-konm.wav"
    ,"/home/bmh/Desktop/cabinet_WebApp/media/6_song_n1M8E0Q.wav"
    ,"/home/bmh/Desktop/cabinet_WebApp/media/7_ahang-o-dos-dashti.wav"
    ,"/home/bmh/Desktop/cabinet_WebApp/media/8_esmet-chie_.wav"
    ,"/home/bmh/Desktop/cabinet_WebApp/media/9_man-mikham-bkhabam-dg.wav"
    ,"/home/bmh/Desktop/cabinet_WebApp/media/10_khodafez-kocholo.wav"
    ,"/home/bmh/Desktop/cabinet_WebApp/media/shutup.wav"]

def play_sound(data):
    text = data.data
    if text.find("shutup") == -1:
        pygame.mixer.Sound.play(pygame.mixer.Sound(data.data))
    elif text.find("shutup") != -1:
        stop_sound()

def player(arg):
    pygame.mixer.Sound.play(pygame.mixer.Sound(sounds[arg]))
    send_step(arg)


def stop_sound():
    pygame.mixer.stop()

def auto_mode():
    
    global t1,t2,t3,t4,t5,t6,t7,t8,t9,t10
    player(0)
    t1=threading.Timer(3, player, args=[1]).start()
    t2=threading.Timer(5.5, player, args=[2]).start()
    t3=threading.Timer(8, player, args=[3]).start()
    t4=threading.Timer(10, player, args=[4]).start()
    t5=threading.Timer(13, player, args=[5]).start()
    t6=threading.Timer(123, player, args=[10]).start()
    t7=threading.Timer(126, player, args=[6]).start()
    t8=threading.Timer(129, player, args=[7]).start()
    t9=threading.Timer(132, player, args=[8]).start()
    t10=threading.Timer(135, player, args=[9]).start()


def auto(data):
    if(data.data == "auto"):
        auto_mode()
    elif(data.data == "manual"):
        pygame.mixer.stop()
        t1.cancel()
        t2.cancel()
        t3.cancel()
        t4.cancel()
        t5.cancel()
        t6.cancel()
        t7.cancel()
        t8.cancel()
        t9.cancel()
        t10.cancel()

def stop_function(data):
    if data.data == 'stop_test':
        pygame.mixer.stop()

def send_step(num):
    auto_publisher.publish("%s"%num)

def ros_init():

    global auto_publisher

    rospy.init_node('audio_player', log_level=rospy.DEBUG)
    rospy.Subscriber("web/parrot_voice_commands", String, play_sound, queue_size=10)
    rospy.Subscriber('web/parrot_command_type', String, auto, queue_size=10)
    rospy.Subscriber("web/stage", String, stop_function, queue_size=10)
    auto_publisher = rospy.Publisher('auto_mode', String, queue_size=10)


def pygame_init():
    pygame.mixer.init()
    if pygame.mixer.get_init() is None:
        print("mixer initialization is NOT successful")



if __name__ == "__main__":
    ros_init()
    pygame_init()
    rospy.spin()