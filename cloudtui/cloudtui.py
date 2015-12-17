from metamanager.metamanager import MetaManager

class CloudTUI:

    def start(self):
        platform = self.show_menu()
        manager = MetaManager(platform)

        while(True):
            manager.show_menu()

    def show_menu(self):
        global kill

        print("******************** CloudTUI-FTS ********************\n")
        print("Please select the Cloud platform that you want to use:")

        print("1) OpenStack")
        print("2) Eucalyptus")

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
        2: 'Eucalyptus',
        1: 'Openstack'
      }[platform]
