#!/usr/bin/env python

# Write a publisher node (Python script) that makes the simulated Husky robot in Gazebo move
# with a linear speed of 0.2 m/s until it hits one of the walls.  Call it move_husky.py and save it
# in the scripts folder of your my_husky_yourlastname package. [Hint: Use the topic
# cmd_vel to send a geometry_msgs::Twist message to the Husky robot
import rospy
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

scan_data = ""
started = False

def callback(data):
    global scan_data, started
    scan_data = data
    if (not started):
        started = True

def colliding():
    global scan_data, started
    search_angle = 0.436332 # in radians, -15 to 15 degrees for collision detection
    range = 0.5 # distance to classify collisions
    if (not started):
        return True
    index = round((scan_data.angle_max - search_angle) / scan_data.angle_increment) 
    scan_range = scan_data.ranges[index:len(scan_data.ranges)-index] # get a forward facing laser beam
    for x in scan_range:
        if x < range:
            return True
    return False

def talker():
    global scan_data
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        speed = Twist(Vector3(0.2,0.2,0.0), Vector3())
        if (not colliding()):
            rospy.loginfo(speed)
            pub.publish(speed)
        rate.sleep()

def listener():
    rospy.init_node('move_husky', anonymous=True)
    rospy.Subscriber('scan', LaserScan, callback)

if __name__ == '__main__':
    listener()
    try:
        talker()
    except rospy.ROSInterruptException:
        pass