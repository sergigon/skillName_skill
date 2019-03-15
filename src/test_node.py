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

# Skill libraries
from skill.skill import Skill, ActionlibException, CONDITIONAL
import rospy
import rospkg
import actionlib

# Messages
from std_msgs.msg import String, Empty
import skillName_msgs.msg ############# Cambiar esto #############

pkg_name = 'skillName_skill' ############# Cambiar esto #############

# Skill variables
# declare this only if the name is different of 'pkg_name'
skill_name = "skillName_skill" ############# Cambiar esto #############

class SkillNameSkill(Skill): ############# Cambiar esto #############

	_feedback = skillName_msgs.msg.SkillNameFeedback() ############# Cambiar esto #############
	_result = skillName_msgs.msg.SkillNameResult() ############# Cambiar esto #############

	def __init__(self):
		"""
		Init method.
		"""

		# class variables
		self._as = None
		self._out = False
		
		# init the skill
		Skill.__init__(self, skill_name, CONDITIONAL)
	
	def pause_exec(self):
		"""
		Callback called when a pause is requested.
		"""

		pass

	def resume_exec(self):
		"""
		Callback called when a resume is requested.
		"""

		pass

	def create_msg_srv(self):
		"""
		Callback called when skill is started.
 		"""
 		rospy.loginfo("Start requested")
		
		# publishers and subscribers
		self.ca_pub = rospy.Publisher(
		    "hri_manager/ca_activations", CA, queue_size=1) # CA publisher
		self.ca_deactivation_pub = rospy.Publisher(
		    "hri_manager/ca_deactivations", String, queue_size=1) # CA deactivation publisher
		# servers and clients

		# actions
		if not self._as:

			self._as = actionlib.SimpleActionServer(pkg_name, skillName_msgs.msg.SkillNameAction, execute_cb=self.execute_cb, auto_start=False) ############# Cambiar esto #############
			# start the action server
			self._as.start()

	def shutdown_msg_srv(self):
		"""
		Callback called when skill is stopped.
		"""

		# publishers and subscribers
		# FIXME: do not unregister publishers because a bug in ROS
		# self.__test_pub.unregister()
		
		rospy.loginfo("Stop requested")
		# servers and clients


	def execute_cb(self, goal): # Se activa cuando le envias un goal a la skill
		"""
		Callback of the node. Activated when a goal is received

        	@param goal: skillName_skill goal.
		"""
		# Init skill variables
		self._out = False
	
		# Init result and feedback
		# -- Result default values -- #
		self._result.skill_result = self._result.SUCCESS # Success
		# -- Feedback default values -- #
		self._feedback.app_status = 'start_ok'
		self._feedback.percentage_completed = 0
		self._feedback.engagement = True
			
		####################### Skill active #######################
		if self._status == self.RUNNING:
			print ("Running...")
			###################### Exec loop #######################
			while not self._out:
			try:
				############# State Preempted checking #############
				# If goal is in Preempted state (that is, there    #
				# is a goal in the queue or the actual goal is     #
				# cancelled), the exception is activated.          #
				####################################################
				if self._as.is_preempt_requested():
					print("Preempt requested")
					raise ActionlibException
				#==================================================#
				
				##################### Process goal #####################
            			rospy.loginfo('Goal: %s' % goal)
				self._counter += 1
				print("self._counter: " + str(self._counter))
				if self._counter >= 20:
					self._result.result = True
					self._out = True

				#==================================================#
	
				#################### Exceptions ####################
                		### Preempted or cancel:
				except ActionlibException:
					rospy.logwarn('[%s] Preempted or cancelled' % pkg_name)                 
					# FAIL
					self._result.skill_result = self._result.FAIL # Fail
					self._feedback.app_status = 'cancel_ok'
					self._out = True # Salgo del loop
				#=================== Exceptions ===================#
			#===================== Exec loop ======================#

		#==================== Skill active ========================#

		##################### Skill NOT active #####################
		else:
			rospy.logwarn("[%s] Cannot send a goal when the skill is stopped" % pkg_name)
			# ERROR
			self._result.skill_result = self._result.FAIL # Fail
		#==========================================================#

		#### Result and feedback sending and goal status update ####
		if self._result.skill_result == self._result.SUCCESS:
		    rospy.logdebug("setting goal to succeeded")
		    self._feedback.app_status = 'completed_ok'
		    self._as.publish_feedback(self._feedback)
		    self._as.set_succeeded(self._result)
		else:
		    rospy.logdebug("setting goal to preempted")
		    self._feedback.app_status = 'completed_fail'
		    self._as.publish_feedback(self._feedback)
		    self._as.set_preempted(self._result)
		rospy.loginfo("#############################")
		rospy.loginfo("######## Result sent ########")
		rospy.loginfo("#############################")


if __name__ == '__main__':

	try:
		# start the node
		rospy.init_node(skill_name)
		rospy.loginfo('[' + pkg_name + ': ' + skill_name + ']')

		# create and spin the node
		node = SkillNameSkill() ############# Cambiar esto #############
		rospy.sleep(1)
        
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
		    rate.sleep()

	except rospy.ROSInterruptException:
		pass
