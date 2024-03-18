

import rospy 
import math
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan 

class nn_epuck:
    def __init__(self):
        
        self.subScan = rospy.Subscriber('/scan',LaserScan,self.scan_callback)
        self.scan = LaserScan()

        self.pubVel = rospy.Publisher('/cmd_vel',Twist,queue_size=10)
        self.vel = Twist()

        self.v = np.array([[0.0]]*2)
        self.dis = np.array([[0.0]]*8)
        self.alpha = np.array([
            [0.01, 0.02, 0.01, 0.01, 0.01, 0.03, 0.05, 0.02], 
            [0.02, 0.05, 0.03, 0.01, 0.01, 0.01, 0.02, 0.01]
        ])
        self.noise = np.array([[0.0], [0.0]])
        self.v0 = np.array([[0.0], [0.0]])

        self.rWheel = [0.033, 0.033]
        self.L = 0.14

        self.vL_max = 0.2
        self.v_max = 0.07
        self.omage_max = 0.2

        rospy.on_shutdown(self.stop)

    def scan_callback(self, msg):
        self.scan = msg
        self.dis[0,0] = self.scan.ranges[341]
        self.dis[1,0] = self.scan.ranges[305]
        self.dis[2,0] = self.scan.ranges[269]
        self.dis[3,0] = self.scan.ranges[209]
        self.dis[4,0] = self.scan.ranges[149]
        self.dis[5,0] = self.scan.ranges[89]
        self.dis[6,0] = self.scan.ranges[54]
        self.dis[7,0] = self.scan.ranges[18]
    
    def process_vel(self):
        print('--------------')
        self.v = self.v0 + np.matmul(self.alpha, self.dis) + self.noise

        vL = self.v[0,0]
        vR = self.v[1,0]
        
        print(f'pre_linear: {vL, vR}')
        if (vL > self.vL_max):
            vL = self.vL_max
        if (vL < -self.vL_max):
            vL = -self.vL_max

        
        if (vR > self.vL_max):
            vR = self.vL_max
        if (vR < -self.vL_max):
            vR = -self.vL_max

        v = (vL*self.rWheel[0] + vR*self.rWheel[1]) / (self.rWheel[0] + self.rWheel[1])
        if (v > self.v_max):
            v = self.v_max
        if (v < -self.v_max):
            v = -self.v_max

        omega = (vL - vR) / self.L
        if (omega > self.omage_max):
            omega = self.omage_max
        if (omega < -self.omage_max):
            omega = -self.omage_max

        self.vel.linear.x = v 
        self.vel.angular.z = omega
        
        print(f'linear: {v}')
        print(f'angular: {omega}')

        self.pubVel.publish(self.vel)
    
    def stop(self):
        self.vel.linear.x = 0.0
        self.vel.angular.z = 0.0
        self.pubVel.publish(self.vel)

if __name__ == "__main__":
    rospy.init_node('nn_epuck',anonymous=False)
    rate = 10
    r = rospy.Rate(rate)
    epuck = nn_epuck()
    while not rospy.is_shutdown():
        epuck.process_vel()
        r.sleep()


        





