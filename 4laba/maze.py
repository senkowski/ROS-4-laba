#!/usr/bin/env python

import rospy
import math
import time
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
a = 0

class Robot:
	def __init__(self):
        	rospy.init_node('antpot', anonymous=True)
        	self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        	self.pose_subscriber = rospy.Subscriber('/base_scan', LaserScan, self.update_pose)
        	self.pose = LaserScan()
        	for i in range(36):
        		self.pose.ranges.append(0)
        	self.rate = rospy.Rate(10)
		self.dist_forward=0
		self.dist_zad=10
		self.dist_pered=10

	def update_pose(self, data):
        	self.pose = data
		self.dist_forward=(self.pose.ranges[15]+self.pose.ranges[16])/2 
		self.dist_zad=self.pose.ranges[4] 
		self.dist_pered=self.pose.ranges[13] 
	

	def labyrint(self):	

		vel_msg = Twist()
		if (math.fabs(self.dist_zad-self.dist_pered)<0.5) and (self.dist_forward>1):
			if self.dist_pered<2:
				print ('move_left')
				print ('pered', self.dist_pered)
				print ('zad', self.dist_zad)
				print ('front', self.dist_forward)
				vel_msg.linear.x = 0
				vel_msg.linear.y = 0
				vel_msg.linear.z = 0
				vel_msg.angular.x = 0
				vel_msg.angular.y = 0
				vel_msg.angular.z = 0.1
			print ('move_forward') 
			print ('pered', self.dist_pered)
			print ('zad', self.dist_zad)
			print ('front', self.dist_forward)
			vel_msg.linear.x = 1
			vel_msg.linear.y = 0
			vel_msg.linear.z = 0
			vel_msg.angular.x = 0
			vel_msg.angular.y = 0
			vel_msg.angular.z = 0
		else:
			if (self.dist_zad>self.dist_pered) and (self.dist_forward>1):
				print ('move_left')
				print ('pered', self.dist_pered)
				print ('zad', self.dist_zad)
				print ('front', self.dist_forward)
				vel_msg.linear.x = 0
				vel_msg.linear.y = 0
				vel_msg.linear.z = 0
				vel_msg.angular.x = 0
				vel_msg.angular.y = 0
				vel_msg.angular.z = 0.1
			
			else:
				if (self.dist_zad<self.dist_pered) and (self.dist_forward>1):
					global a
					a=a+1
					print ('move_right')
					print ('pered', self.dist_pered)
					print ('zad', self.dist_zad)
					print ('front', self.dist_forward)
					vel_msg.linear.x = 0
					vel_msg.linear.y = 0
					vel_msg.linear.z = 0
					vel_msg.angular.x = 0
					vel_msg.angular.y = 0
					vel_msg.angular.z = -0.1
			
				else:
					print ('move_left')
					print ('pered', self.dist_pered)
					print ('zad', self.dist_zad)
					print ('front', self.dist_forward)
					vel_msg.linear.x = 0
					vel_msg.linear.y = 0
					vel_msg.linear.z = 0
					vel_msg.angular.x = 0
					vel_msg.angular.y = 0
					vel_msg.angular.z = 0.1
		if a>50:				
			global a 
			a = 0
			print ('move_forward')
			vel_msg.linear.x = 1
			vel_msg.linear.y = 0
			vel_msg.linear.z = 0
			vel_msg.angular.x = 0
			vel_msg.angular.y = 0
			vel_msg.angular.z = 0

		self.velocity_publisher.publish(vel_msg)
		self.rate.sleep()
		return
	
	def move(self):
		while not rospy.is_shutdown():
			#time.sleep(0.5)
			self.labyrint()

if __name__ == '__main__':
    try:
	x = Robot()
	x.move()
    except rospy.ROSInterruptException:
        pass

