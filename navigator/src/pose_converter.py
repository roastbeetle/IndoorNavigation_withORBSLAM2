#!/usr/bin/env python
#-*- coding:utf-8 -*-
from PIL import Image
import rospy
from std_msgs.msg import Int8
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PoseWithCovarianceStamped
from std_msgs.msg import Int32MultiArray as intarr   

import tf
import cv2
import numpy as np
import math
import random
import sys


prev_pos_x = 0.0
prev_pos_y = 0.0
prev_pos_z = 0.0

start_pub = rospy.Publisher('initialpose',PoseWithCovarianceStamped,queue_size = 1)
target_pub = rospy.Publisher('move_base_simple/goal',PoseStamped,queue_size = 1 )

start_pose = PoseWithCovarianceStamped()
start_pose.header.frame_id = "map"

target_pose = PoseStamped()
target_pose.header.frame_id = "map"


scale = 10
tp = [0,0,0]
#f = open('/home/lb/nin_ws/src/localizat/src/simulation.txt','r')
def tp_callback(data):
    tp[0] = (data.data[0]-250)*2
    tp[1] = -(data.data[1]-250)*2

def sp_callback(data):
    print('callback')
    start_pose.pose.pose.position.x = data.position.x*scale
    start_pose.pose.pose.position.y = data.position.z*scale
    start_pose.pose.pose.position.z = 0.0

    quaternionS = (data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w)
    eulerS = tf.transformations.euler_from_quaternion(quaternionS)
    quaternionS2 = tf.transformations.quaternion_from_euler(0, 0, eulerS[2]+math.pi/2)

    start_pose.pose.pose.orientation.x = quaternionS2[0]
    start_pose.pose.pose.orientation.y = quaternionS2[1]
    start_pose.pose.pose.orientation.z = quaternionS2[2]
    start_pose.pose.pose.orientation.w = quaternionS2[3]

    target_pose.pose.position.x = int(tp[0])
    target_pose.pose.position.y = int(tp[1])
    target_pose.pose.position.z = 0.0


    target_pose.pose.orientation.x = 0.0
    target_pose.pose.orientation.y = 0.0
    target_pose.pose.orientation.z = 0.0
    target_pose.pose.orientation.w = 1.0
    
    if(target_pose.pose.position.x != 0 and target_pose.pose.position.y !=0):
        start_pub.publish(start_pose)
        target_pub.publish(target_pose)

def simulate(rate):
    #pointS1 = f.readline().strip().split(' ')
    #pointS2 = f.readline().strip().split(' ')
    
    #if not pointS2:
    #    f.close()

    point1 = [130,150]
    #point1[0] = int(float(pointS1[0]))
    #point1[1] = int(float(pointS1[1]))

    point2 = [0,0]
    #point2[0] = int(float(pointS2[0]))
    #point2[1] = int(float(pointS2[1])) 

    pointOri = math.atan2(point2[1]-point1[1],point2[0]-point1[0])
    
    quat = tf.transformations.quaternion_from_euler(0, 0, pointOri)
    start_pose.pose.pose.orientation.x = quat[0]
    start_pose.pose.pose.orientation.y = quat[1]
    start_pose.pose.pose.orientation.z = quat[2]
    start_pose.pose.pose.orientation.w = quat[3]

    start_pose.pose.pose.position.x = point1[0]# + random.randint(-1,1)
    start_pose.pose.pose.position.y = point1[1]# + random.randint(-1,1)
    start_pose.pose.pose.position.z = 0.0
    print(point1,pointOri)

    target_pose.pose.position.x = int(tp[0]*scale)
    target_pose.pose.position.y = int(tp[1]*scale)
    target_pose.pose.position.z = 0.0


    target_pose.pose.orientation.x = 0
    target_pose.pose.orientation.y = 0
    target_pose.pose.orientation.z = 0
    target_pose.pose.orientation.w = 1

    start_pub.publish(start_pose)
    target_pub.publish(target_pose)
    rate.sleep()
		
def publisher(): 
    rospy.init_node('pose_converter')
    rospy.Subscriber("/cur_camera_pose",Pose,sp_callback,queue_size =1)
    rospy.Subscriber("/target_point",intarr,tp_callback,queue_size =1)
    rate = rospy.Rate(5) # 10hz
    rospy.spin()
    #while not rospy.is_shutdown():
    ##    simulate(rate)
    
if __name__=='__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass


