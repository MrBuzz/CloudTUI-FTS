from pkgutil import iter_modules
from inspect import getmembers,isclass
from importlib import import_module
from rules.rulemanager import RuleManager
import platforms
import sys

class MetaManager:

    current = None

    def __init__(self, platform):
        self.all_platforms = self.load_all_platforms()
        self.current_platform = self.all_platforms[platform]()
        self.current_platform.connect()
        self.set_current(platform)
        self.rule_manager = RuleManager()
    def set_current(self, _plat):
        MetaManager.current = _plat

    @staticmethod
    def get_current():
        return MetaManager.current

    def load_all_platforms(self):
        _all_platforms  = { }
        _all_modules = list(iter_modules(platforms.__path__))
        for _mod in _all_modules:
            _module = import_module('.' + _mod[1], platforms.__name__)
            _manager_name = _mod[1][0].capitalize() +_mod[1][1:]
            _manager_class = getattr(_module, _manager_name)
            _all_platforms[_manager_name] = _manager_class
        return _all_platforms

    def print_platforms(self):
        for _platform_name, _platform_obj  in self.all_platforms.items():
            print(_platform_name, _platform_obj)

    def change_platform(self):
        _platforms = list(self.all_platforms.keys())
        i = 1
        print("Wich platform do you want to use?")
        for _plat in _platforms:
            print("{0}) {1}".format(i,_plat))
            i+=1
        _choice = input("> ")
        self.current_platform = self.all_platforms[_platforms[_choice-1]]()
        self.current_platform.connect()
        self.set_current(_platforms[_choice-1])


    def show_menu(self):
        menu_text = """\nWhat would you like to do?
        --------------------------
        1) Create new instance
        2) Show running instances
        3) Start monitor
        4) Stop monitor
        5) Change platform
        6) Manage rules
        7) Exit
        \n"""
        print(menu_text)
        try:
            # user input
            print("Please make a choice: ")
            choice = input()
            if choice == 1:
                self.current_platform.create_new_instance()
            elif choice == 2:
                self.current_platform.print_all_instances()
            elif choice == 3:
                self.current_platform.start_monitor()
            elif choice == 4:
                self.current_platform.stop_monitor()
            elif choice == 5:
                self.change_platform()
            elif choice == 6:
                self.rule_manager.show_menu()
            elif choice == 7:
                exit(0)
            else:
                raise Exception("Unavailable choice!")
        except Exception as e:
            print(e.message)
