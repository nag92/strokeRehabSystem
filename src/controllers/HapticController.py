#!/usr/bin/env python

import rospy
from strokeRehabSystem.msg import *
from geometry_msgs.msg import Pose,Point, WrenchStamped
import math
class HapticController():

    def __init__(self, k_obs, k_goal, d_obs, d_goal ):
        """
        """
        #rospy.init_node("haptics",anonymous=True)
        self.pub = rospy.Publisher("motors_server", WrenchStamped, queue_size=1)
        self.k_obs  = -k_obs
        self.k_goal = k_goal
        self.d_obs  = d_obs
        self.d_goal = d_goal

    def make_force(self,player, obstacles=[],goals=[]):

        forces = WrenchStamped()
        forces.header.frame_id = "master"

        f_y = 0
        f_x = 0

        for g in goals:
            d = math.sqrt( (g.x - player.x)**2 + (g.y - player.y)**2  )
            theta = math.atan2( (g.y - player.y),(g.x - player.x) )
            F = self.k_goal * ( max(self.d_goal - d,0))
            f_y += round(F*math.sin(theta),2)
            f_x += round(F*math.cos(theta),2)

        for obs in obstacles:
            d = math.sqrt( (obs.x - player.x)**2 + (obs.y - player.y)**2  )
            theta = math.atan2( (obs.y - player.y),(obs.x - player.x) )
            F = self.k_obs * ( max(self.d_obs - d,0))
            f_y += round(F*math.sin(theta),2)
            f_x += round(F*math.cos(theta),2)

        [forces.wrench.force.x, forces.wrench.force.y, forces.wrench.force.z] = [ round(f_x,1), 0, -round(f_y, 1) ]
        self.pub.publish(forces)
