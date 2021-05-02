#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import random

#some variables:
throttle = 10
v_min = -10
v_max = 10
duration= 1

def move():
    #create a node
    rospy.init_node('crazy_turle', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    for i in range(10):
        vel_msg.linear.y = random_speed()
        vel_msg.linear.x = random_speed()
        vel_msg.angular.x = random_speed()

        velocity_publisher.publish(vel_msg)
        print("Command:",vel_msg)
        rospy.sleep(duration)


    print("Oioi:",vel_msg)

def random_speed():
    random_val = random.randint(-10,10)
    return random_val



if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException: pass