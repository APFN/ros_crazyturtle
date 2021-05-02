#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import random
from turtlesim.msg import Pose
import math


#some variables:
throttle = 10
v_min = -10
v_max = 10
duration = 1
avoid = False
degrees = 0
turn_ind_degrees = 0


def random_speed():
    random_val = random.random()
    return random_val

def opposite_angle (degrees):
    if(degrees>0):
        return degrees-180
    else:
        return degrees+180



def pose_callback(pose):
    global avoid, degrees, turn_ind_degrees
    if(pose.x <= 0.1 or pose.x >= 9.9 or pose.y <=  0.1 or pose.y >= 9.9): 
        theta = pose.theta   
        degrees=theta*180/math.pi             
        if(avoid==False):
            turn_ind_degrees=opposite_angle(degrees)       
            avoid = True
            #print("theta:", theta)
            #print("X:", pose.x)
            #print("Y:", pose.y)

def avoidCollision():
    global avoid
    vel_msg = Twist() 
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    vel_msg.linear.y = 0
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)
    

    print("degrees",degrees)
    print("--------Turn:",turn_ind_degrees)

    if(turn_ind_degrees-10 <= degrees <= turn_ind_degrees+10):
        print("true:")
        avoid = False  
        vel_msg.linear.y = 0
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        velocity_publisher.publish(vel_msg)
        
    else: 
        vel_msg.angular.z = 0.5
        velocity_publisher.publish(vel_msg)
        rospy.sleep(0.2)   
        print("ELSE")

def move():
    #create a node
    rospy.init_node('crazy_turle', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/turtle1/pose',Pose, pose_callback)
    vel_msg = Twist() 

    while not rospy.is_shutdown():
        while (avoid):
            avoidCollision()
            print("avoid")

        
        vel_msg.linear.x = random_speed() * throttle
        #vel_msg.linear.y = random_speed() * throttle
        #vel_msg.angular.z = random_speed() 

        velocity_publisher.publish(vel_msg)
        print("Command:",vel_msg)

        rospy.sleep(duration)   
        

if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException: pass