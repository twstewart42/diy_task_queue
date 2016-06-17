#!/usr/bin/evn python
#################
#
# runtask.py - Python Class that will execute the message
# Author: Tom Stewart
# You have my permission to use this in any way. Open Source
#
###################


from __future__ import absolute_import
import subprocess
import os

def demote(user_uid, user_gid):
    'Demote task to run as non-root user'
    def result():
        #print('starting demotion')
        os.setgid(user_gid)
        os.setuid(user_uid)
        #print('finished demotion')
    return result

class Tasker:
	'Sets up task to run on host'

	def __init__(self, uid, taskstr):
		self.uid = uid
		self.taskstr = taskstr

	def task_do(self):
		gid = 714
		uid = 714
		print self.uid, self.taskstr
		run_task = subprocess.Popen([self.taskstr], preexec_fn=demote(uid, gid), shell=True, stdout=subprocess.PIPE)
		taskout, taskerr = run_task.communicate()
		print taskout, taskerr


#task1 = Tasker(12345, "ping -c 4 8.8.8.8; ps faux | grep ping")
#task1.task_do()
	
