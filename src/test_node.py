#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Elena Velázquez and Sergio González"
__copyright__ = "Social Robots Group. Robotics Lab. University Carlos III of Madrid"
__credits__ = ["Elena Velázquez and Sergio González"]
__license__ = "LEUC3M v1.0"
__version__ = "0.0.0"
__maintainer__ = "Elena Velázquez and Sergio González"
__email__ = "serigon@ing.uc3m.es"
__status__ = "Development"

#from functions.dms_functions import my_import
from skill.skill import Skill, ActionlibException, CONDITIONAL
from std_msgs.msg import String, Empty
from std_srvs.srv import Empty
from etts_msgs.msg import Utterance
from perception_msgs.msg import PerceptionMessage
from interaction_msgs.msg import CA
from common_msgs.msg import KeyValuePair
import key_value_pairs as kvpa

import roslib
import rospy
import actionlib
import multimedia_msgs.msg ############# Cambiar esto #############

pkg_name = 'test_skill' ############# Cambiar esto #############
roslib.load_manifest(pkg_name)

# declare this only if the name is different of 'pkg_name'
skill_name = "test_skill" ############# Cambiar esto #############

### rospy.loginfo("Subscriber: " + msg.data + str(self.__counter))

class TestSkill(Skill): ############# Cambiar esto #############

	_feedback = multimedia_msgs.msg.TestFeedback() ############# Cambiar esto #############
	_result = multimedia_msgs.msg.TestResult() ############# Cambiar esto #############

	def __init__(self):
		"""
		Init method.
		"""
		# init the skill
		Skill.__init__(self, skill_name, CONDITIONAL)

		# class variables
		self._as = None
		self._counter = 0
		self._out = False

	def create_msg_srv(self):
		"""
		This function has to be implemented in the children.
 		"""
 		print("create_msg_srv")
		# publishers and subscribers
		# servers and clients

		# actions
		if not self._as:

			self._as = actionlib.SimpleActionServer(pkg_name, multimedia_msgs.msg.TestAction, execute_cb=self.execute_cb, auto_start=False) ############# Cambiar esto #############

			# start the action server
			self._as.start()

	def shutdown_msg_srv(self):
		"""
		This function has to be implemented in the children.
		"""

		# publishers and subscribers
		# FIXME: do not unregister publishers because a bug in ROS
		# self.__test_pub.unregister()

		# servers and clients


	def execute_cb(self, goal):
		"""
		Spinner of the node.
		"""
		rospy.loginfo('[TEST SKILL]') ############# Cambiar esto #############
	
		# default values (SUCCESS)
		self._result.result = False
		self._feedback.feedback = 0
		
		# Cojo informacion del goal recibido
		################################################
		if  goal.command != '':
			rospy.loginfo("goal:" + str(goal.command))
		else:
			rospy.loginfo("goal vacio") 

		while not self._out:
			# sleep 2 seconds
			rospy.sleep(2.0)
			
			print("self._status: "+ str(self._status) + ", self.RUNNING:" + str(self.RUNNING))
			if self._status == self.RUNNING:
				print ("Running...")
				try:
					self._counter = self._counter + 1
					print("self._counter: " + str(self._counter))
					if self._counter >= 20:
						self._result.result = True
						self._out = True

					if self._as.is_preempt_requested():
						print("Preempt requested")
						raise ActionlibException

				except ActionlibException:
					
					rospy.logwarn('[%s] Preempted or cancelled' % pkg_name)                 
					# FAIL
					self._result.result = 1
					self._feedback.feedback = 0
					

			else:
				rospy.logwarn("[%s] Cannot send a goal when the skill is stopped" % pkg_name)
				# ERROR
				self._result.result = -1
				self._feedback.feedback = 0


			self._feedback.feedback = self._counter
			self._as.publish_feedback(self._feedback)

		print("Fuera del while")

		if self._result.result:
			self._as.set_succeeded(self._result)
		else:
			rospy.logdebug("setting goal to preempted")
			self._as.set_preempted(self._result)


		#Inicializacion variables
		self._counter = 0
		self._out = False



if __name__ == '__main__':

	try:
		# start the node
		rospy.init_node(skill_name)

		# create and spin the node
		node = TestSkill() ############# Cambiar esto #############
		rospy.spin()

	except rospy.ROSInterruptException:
		pass


		'''
		# Akinator
			self._feedback.progression = self.progression
			self._as.publish_feedback(self._feedback)

		if self._result.result:
			self._as.set_succeeded(self._result)
		else:
			rospy.logdebug("setting goal to preempted")
			self._as.set_preempted(self._result)
			'''
