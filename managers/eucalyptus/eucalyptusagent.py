__author__ = 'Giorgio Gambino'

import logging

class EucalyptusAgent:

    def __init__(self,manager):
        self.manager = manager
        self.loop = True

    def stop(self):
        self.loop = False

    def run(self,cmd_queue):
        try:
            while self.loop:
                command = cmd_queue.get()
                logging.debug("Command received"+ str(command))
                self.execute_command(command)

        except Exception, e:
            logging.error("Error %s:" % e.args[0])
            print("An error occured. Please see logs for more information")

    def get_action_method(self, action):
        return {
            'clone': self.manager.clone_instance,
            'alarm': self.manager.alarm,
            'stop': self.stop
        }[action]

    def execute_command(self, command):
        logging.debug("Executing command {0}".format(command))
        action_method = self.get_action_method(command['command'])
        action_method(command['resource_id'])
