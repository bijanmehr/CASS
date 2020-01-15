#!/bin/bash

echo "start CASS"
echo "start ROS packages"
source /home/cabinet/catkin_ws/devel/setup.bash
roslaunch cabinet cabinet.launch
