#!/usr/bin/env python
from ctypes import resize
from PIL import Image
import rospy
from std_msgs.msg import Int32MultiArray as intarr
from nav_msgs.msg import Path
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PoseWithCovarianceStamped
from rospy.core import is_shutdown
import tf
import cv2
import numpy as np
import math
import random

#parameter
scale = 10
re_path = 4
arr_cnt = 0

#initialize list
mp_list = []
ref_path = []
prev_cam_pose = [0,0,0]
cam_pose = [0,0,0] # x y orientation

#initialize counter
do = 0
noise_cnt = 0
voice_backcounter = 0
voice_distcounter = 0
voice_arricounter = 0

inst_pub = rospy.Publisher('instruct',intarr,queue_size = 1)
simple_path_pub = rospy.Publisher('simple_path',Path,queue_size = 1)

def lineFromPoints(P, Q):
    line = []
    a = Q[1] - P[1]
    b = P[0] - Q[0]
    c = -a*(P[0]) - b*(P[1])

    if(P[0] == Q[0] and P[1] == Q[1]):
        return line
    line.append(a)
    line.append(b)
    line.append(c)
    return line

def shortest_distanceLP(x1, y1, a, b, c):
    d = abs((a * x1 + b * y1 + c)) / (math.sqrt(a * a + b * b))
    return d

def shortest_distancePP(x1, y1, x2, y2):
    d = math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
    return d

def shortest_distanceSP(x1,y1,x2,y2,px,py):
    len = shortest_distancePP(x1,y1,x2,y2)
    if(len == 0):
        return shortest_distancePP(x1,y1,px,py)
    prj = ((px-x1)*(x2-x1)+(py-y1)*(y2-y1))/len
    if(prj<0):
        return shortest_distancePP(x1,y1,px,py)
    elif(prj>len):
        return shortest_distancePP(x2,y2,px,py)
    else:
        return abs(((-1)*(px-x1)*(y2-y1)+(py-y1)*(x2-x1))/len) 

def det_sequence(path,idx,px,py,end):
    if not idx:
        return 0
    if(shortest_distancePP(end[0],end[1],px,py))< scale:
        return 1000
    
    seq = 0
    dist_min = scale*re_path
    for i in range(len(idx)-1):
        dist = (shortest_distanceSP(path[idx[i]][0],path[idx[i]][1],path[idx[i+1]][0],path[idx[i+1]][1],px,py))
        if dist<dist_min:
            dist_min = dist
            seq = i+1
    
    return seq
                                    
def mxpoint(data,start,end):
    if start == end:
        return 0
    dist_max = 0.0
    max = 0
    ep = data[end]
    sp = data[start]
    line = lineFromPoints(sp, ep)
    for j in range(start,end):
        cur = data[j]
        dist = shortest_distanceLP(cur[0],cur[1], line[0], line[1], line[2])
        #print(j, cur.pose.position.x, cur.pose.position.y, line, dist)
        if dist>dist_max and dist>scale*2:
            dist_max = dist
            max = j
    return max

def simplify_path(data, start, end, mp_list):
    mp = mxpoint(data, start, end)
    if mp is 0:
        return 0
    else:
        mp_list.append(mp)
        simplify_path(data, start, mp, mp_list)
        simplify_path(data, mp, end, mp_list)
        return 0

def path_callback(data):
    global do
    global mp_list
    global ref_path
    global arr_cnt
    global prev_seq
    global simple_path

    path = []
    back = 0
    cur_dis = 0
    left_right = 2
    for i in range(len(data.poses)):
        pt = [data.poses[i].pose.position.x,data.poses[i].pose.position.y]
        path.append(pt)

    if (do == 0):
        seq = det_sequence(path, mp_list, cam_pose[0],cam_pose[1],path[-1])
        prev_seq = seq
    else:
        seq = det_sequence(ref_path, mp_list, cam_pose[0],cam_pose[1],path[-1])
        prev_seq = seq
    print('corner:',mp_list,'  sequence:',seq)

    # when start or away from path, do path_planning 
    if(do == 0 or seq == 0):
        print('re_pathplanning...')
        do = 1 
        simple_path = Path()
        simple_path.header.frame_id = "map"
        end = len(path)-1
        start = 0
        mp_list = [start, end]
        simplify_path(path, start, end, mp_list)
        mp_list.sort()
        for idx in mp_list:
            p = PoseStamped()
            p.pose.position.x = path[idx][0]  
            p.pose.position.y = path[idx][1]  
            simple_path.poses.append(p)
        
        ref_path = path
    
    # navigation
    if(seq!=1000):
        cur_start = [ref_path[mp_list[seq-1]][0],ref_path[mp_list[seq-1]][1]]
        cur_goal = [ref_path[mp_list[seq]][0],ref_path[mp_list[seq]][1]]
        cur_ori = math.atan2(cur_goal[1]-cur_start[1],cur_goal[0]-cur_start[0])
        cur_dis = int(shortest_distancePP(cam_pose[0],cam_pose[1],cur_goal[0],cur_goal[1])/scale)
        angle = cam_pose[2]-cur_ori

        if abs(angle)>0.75*math.pi:
            back = 1

        if(seq<len(mp_list)-1):
            next_goal = [ref_path[mp_list[seq+1]][0],ref_path[mp_list[seq+1]][1]]
            next_ori = math.atan2(next_goal[1]-cur_goal[1],next_goal[0]-cur_goal[0])
            next_angle = cur_ori - next_ori
            if next_angle>math.pi/6:
                left_right = 1
            elif next_angle < -math.pi/6:
                left_right = 0
            print('moving from',cur_start,'to',cur_goal,' distacne',cur_dis,' with angel ',left_right)
        else:
            print('moving from',cur_start,'to',cur_goal,' distacne',cur_dis )
    
    # arrive
    else:
        arr_cnt = arr_cnt +1
        if arr_cnt == 4:
            arr_cnt = 0
        print('arrrivee')

    # publish
    instruct = intarr()
    instruct.data = [seq, back, cur_dis, left_right ,arr_cnt]
    print(instruct.data)
    inst_pub.publish(instruct)
    simple_path_pub.publish(simple_path)

def pose_callback(data):
    global noise_cnt
    global prev_cam_pose
    global cam_pose

    cam_pose[0] = data.pose.pose.position.x
    cam_pose[1] = data.pose.pose.position.y
    quaternionS = (data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.z, data.pose.pose.orientation.w)
    cam_pose[2] = tf.transformations.euler_from_quaternion(quaternionS)[2]

    d = shortest_distancePP(cam_pose[0],cam_pose[1],prev_cam_pose[0],prev_cam_pose[1])
    if noise_cnt == 2:
        noise_cnt = 0
        prev_cam_pose =cam_pose
    
    elif d > scale:
        cam_pose = prev_cam_pose
        noise_cnt = noise_cnt + 1

 
def navigation(): 
    rospy.init_node('navigation')
    rospy.Subscriber('initialpose',PoseWithCovarianceStamped,pose_callback,queue_size =1)
    rospy.Subscriber("/nav_path",Path,path_callback,queue_size =1)
    rospy.spin()
    
if __name__=='__main__':
    try:
        navigation()
    except rospy.ROSInterruptException:
        pass
