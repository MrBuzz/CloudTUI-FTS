#from managers.eucalyptus.eucalyptusmanager import EucalyptusManager
#from managers.nimbus.nimbusmanager import NimbusManager
#from managers.openstack.openstackmanager import OpenstackManager
from metamanager.metamanager import MetaManager
#import metamanager.platforms

__author__ = 'Davide Monfrecola'


class CloudTUI:

    def __init__(self):
        pass

    def start(self):
        platform = self.show_menu()
        # Create a new instance according to user platform selection
        manager = MetaManager(platform)
        #manager.print_platforms()
        while(True):
            manager.show_menu()

    def show_menu(self):
        global kill

        print("******************** CloudTUI-FTS ********************\n")
        print("Please select the Cloud platform that you want to use:")

        print("1) OpenStack")
        print("2) Eucalyptus")
        #print("3) Nimbus")

        while True:
            try:
                # user input
                print("Please make a choice: ")
                choice = input()
                platform = self.get_platform(choice)
                break
            except Exception:
                print("Unavailable choice!")

        return platform

    def get_platform(self, platform):
      return {
        #3: 'NimbusManager',
        2: 'Eucalyptus',
        1: 'Openstack'
      }[platform]
