# USING TO PLOT DATA FROM TOPIC 

import rospy
import matplotlib.pyplot as plt
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PointStamped


class Plotting():
    def __init__(self):

        # Topic
        self.odom_topic = rospy.Subscriber("/odom",Odometry,self.odom_callback)
        
        # Variable 
        self.odom     = Odometry()

        self.a1 = []
        self.a2 = []
        
        self.count = []
        self.step = 1
        
        # Directory to save image result 
        self.save_dir = '/home/manh/doan_ws/src/lvi_fusion/result/img/localization5.png'
        
        rospy.on_shutdown(self.plotting)

    def odom_callback(self, msg):
        self.odom = msg
    
    def imuInc_callback(self, msg):
        self.imuInc = msg
    
    def imu_callback(self, msg):
        self.imu = msg

    def process_vari(self):
        self.a1.append(self.odom.pose.pose.position.x + 2.0)
        self.a2.append(self.odom.pose.pose.position.y - 3.0)
        
        self.b1.append(self.imuInc.pose.pose.position.x)
        self.b2.append(self.imuInc.pose.pose.position.y)

        self.c1.append(self.imu.pose.pose.position.x)
        self.c2.append(self.imu.pose.pose.position.y)

        
    def plotting(self):
        
        m = 5
        n = 1
        k = 1
        plt.figure()

        plt.plot(self.a1[m:len(self.a1)], self.a2[m:len(self.a2)], color='black',label="ref", linewidth = 1.0)
        # plt.plot(self.b1[m:len(self.b1)], self.b2[m:len(self.b2)], color='red',label="imu_incremental", linestyle='dashdot', linewidth=1.0)
        # plt.plot(self.c1[m:len(self.c1)], self.c2[m:len(self.c2)], color='blue', label="imu", linestyle='dotted', linewidth=1.0)

        plt.legend()
        plt.grid(True)
        plt.title("Quỹ đạo tự động tránh vật cản của robot e-puck sử dụng mạng nơ ron")
        plt.xlabel("x [m]")
        plt.ylabel('y [m]')
        # print(len(self.a),len(self.b),len(self.c),len(self.d))
        plt.savefig(self.save_dir,dpi=1000)
        plt.show()
        rospy.loginfo(f'\033[94mImage saved in\033[0m {self.save_dir}')

if __name__ == "__main__":
    rospy.init_node('matplot',anonymous=False)
    rate = 10 
    r = rospy.Rate(rate)

    rospy.loginfo("\033[92mInit Node Plotting...\033[0m")
    

    m = Plotting()
    while not rospy.is_shutdown():
        m.process_vari()
        r.sleep()
    
    rospy.loginfo("\033[92mDone!!!\033[0m")
    