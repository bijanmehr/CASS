#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import pygame
import time


def play_sound(data):
    text = data.data
    if text.find("shutup") == -1:
        pygame.mixer.Sound.play(pygame.mixer.Sound(data.data))

def stop_sound(data):
    pygame.mixer.stop()

def auto_mode():
    pass

def auto(data):
    if(data.data == "auto"):
        auto_mode()

def ros_init():
    rospy.init_node('audio_player', log_level=rospy.DEBUG)
    rospy.Subscriber("web/parrot_voice_commands", String, play_sound, queue_size=10)
    rospy.Subscriber('web/parrot_command_type', String, auto, queue_size=10)
#     rospy.Subscriber("audio_player/play_sound", String, play_sound, queue_size=10)
#     rospy.Subscriber("audio_player/stop_sound", String, stop_sound, queue_size=10)


def pygame_init():
    pygame.mixer.init()
    if pygame.mixer.get_init() is None:
        print("mixer initialization is NOT successful")



if __name__ == "__main__":
    ros_init()
    pygame_init()
    rospy.spin()