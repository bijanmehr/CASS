import rospy
import os
from datetime import datetime
import csv
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String
from sensor_msgs.msg import CameraInfo




record_stat = 0
bridge = CvBridge()
data_writer = None

def main():
    rospy.init_node('logger')
    rospy.Subscriber('web/stage', String, set_stages)
    rospy.Subscriber('web/dir', String, dir_handler)
    rospy.Subscriber('web/wheel_status ', String, lightwheel_status_log)
    rospy.Subscriber('web/parrot_command_name', String, parrot_action_logs)
    rospy.Subscriber('web/parrot_voice_commands', String, parrot_voice_logs)
    rospy.Subscriber("/cam1/image_raw", Image, image_callback_cam1)
    rospy.Subscriber("/cam1/camera_info", CameraInfo, seq_callback_cam1)

def set_stages():
    stage = data.data
    with open(dir + '/log.csv', 'a') as log_file :
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        log_file.write('%s,%d,%d,%s\n'%(date,cam1_frame,cam2_frame,stage))
    return stage
    record_stat += 1
    if record_stat == 1:
        start_record()
    elif record_stat != 4 & record_stat > 1:
        stop_record()
        start_record()
    elif record_stat == 4:
        stop_record()
    else:
        pass

def dir_handler():
    dir = os.path.expanduser(data.data)
    if not os.path.exists(dir):
        rospy.logwarn('directory is not exist!')
    else:
        return dir
        with open(dir + '/log.csv', 'a') as log_file :
            log_file.write('time, cam1_frame_num, cam2_frame_num, action\n')
            rospy.loginfo('log file created!('+dir+'/log.csv)')
        
def lightwheel_status_log():
    stat = data.data
    with open(dir + '/log.csv', 'a') as log_file :
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        log_file.write('%s,%d,%d,%s\n'%(date,cam1_frame,cam2_frame,stat))
                
def parrot_action_logs():
    act = data.data
    with open(dir + '/log.csv', 'a') as log_file :
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        log_file.write('%s,%d,%d,%s\n'%(date,cam1_frame,cam2_frame,act))

def parrot_voice_logs():
    act = data.data
    with open(dir + '/log.csv', 'a') as log_file :
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        log_file.write('%s,%d,%d,%s\n'%(date,cam1_frame,cam2_frame,act))

def image_callback_cam1():
    global data_writer,writer_flag
    try:
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        cv2_img = cv2.flip(cv2_img,1)
        if end_process == False:
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

        elif end_process == True :
            try :
                data_writer.release()
            except Exception as e :
                print e


        # Save your OpenCV2 image as a jpeg
        cv2.imshow('camera_image1', cv2_img)

        key = cv2.waitKey(1)

    except CvBridgeError, e:
        print(e)

def seq_callback_cam1():
    global first_seq,current_frame
    if end_process == False:
        if first_seq == -1:
            first_seq = data.header.seq
            cam1_frame = first_seq
        else:
            current_frame = data.header.seq - first_seq
            cam1_frame = current_frame
    else:
        first_seq = -1
        current_frame = 0
    return cam1_frame

def start_record():
    end_process = False
    return end_process

def stop_record():
    end_process = True
    writer_flag = True
    return end_process, writer_flag