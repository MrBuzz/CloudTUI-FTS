import logging
from actionbinder import get_actions

class MetaAgent:
    def __init__(self, manager):
        self.manager = manager
        self.loop = True

    def stop(self):
        self.loop = False

    def run(self, cmd_queue):
        try:
            while self.loop:
                command = cmd_queue.get()
                logging.debug("Command received"+ str(command))
                self.execute_command(command)

        except Exception, e:
            logging.error("Error %s:" % e.args[0])
            print("An error occured. Please see logs for more information")

    def execute_command(self, command):
        try:

            all_actions = get_actions(self.manager.__class__.__name__)
            action_method = getattr(self.manager, all_actions[command['command']])

        except Exception, e:
            print("Error: instance {0} has no action called {1}".format(self.manager.__class__.__name__,e.args[0]))

        else:
            action_method(command['resource_id'])
