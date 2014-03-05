import sys

import roslib; roslib.load_manifest('GuideBot')
import rospy

from kobuki_msgs.msg import SensorState
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import os

class radiosensor:
    
   def __init__(self):
 
     # boolean check to make the robot give warning only once
     self.check = True
     self.hasSpoken = True
     self.vel = Twist()
 
     self.pub = rospy.Publisher('recognizer/output', String)
     self.pub2 = rospy.Publisher('mobile_base/commands/velocity', Twist) 
     #rospy.Subscriber('mobile_base/commands/velocity', Twist, self.LastVelCallback)
     # subscriber for the analog input on the kobuki base
     rospy.Subscriber('mobile_base/sensors/core', SensorState, self.SensorStateCallback)
 
   # saves the last velocity before a stop command is issued when the radio sensor is outside of range 
   #def LastVelCallback(self, msg):
   # if self.check: 
   #    self.vel = msg
   # else: 
   #    return
   
   def SensorStateCallback(self, data):
      #prints intensity range of the radio feedback
      sys.stdout.write("\r\x1b[KAnalog input: [%d]" %(data.analog_input[0]))
      sys.stdout.flush()
      
      # checks the intensity value of the input value and issues commands depending on intensity. Smaller the value the further away the 
      # the sensor is from the receiver      
      if data.analog_input[0] > 70:
         self.check = True
         self.hasSpoken = True
         # resumes the robot's movement when person is in range if the robot had stopped when the radio sensor went out of range       
         #self.pub2.publish(self.vel)
      elif data.analog_input[0] < 30 and data.analog_input[0] > 20 and self.hasSpoken:
         self.hasSpoken = False
         os.system("espeak -v en \"reduce distance to robot\"")
      elif data.analog_input[0] < 10 and self.check:
         self.check = False
         os.system("espeak -v en \"robot stopped waiting for user\"")       
         print('stop')
         self.pub.publish('stop')
        
   
if __name__ == '__main__':
     rospy.init_node("radiosensor")
     Location = radiosensor()
     rospy.spin()




