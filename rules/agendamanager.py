
import policies

class AgendaManager:

    def __init__(self):
        self.agenda_groups = self.load_agenda_groups()

    def load_agenda_groups(self):
        _File = open(policies.__path__[0] + '/agenda-groups' ,'r')
        _file_list = list([_line for _line in _File])
        _File.close()
        return _file_list

    def print_groups(self):
        _i = 1
        for _group in self.agenda_groups:
            print("{0}) {1}\n".format(_i,_group))
            _i += 1

    def write_down(self, _groups):
        _File = open(policies.__path__[0] + '/agenda-groups' ,'w')
        _File.seek(0)
        _File.truncate()

        for _group in _groups:
            _File.write(_group + '\n')

        _File.close()

    def do_delete_group(self, _group):
        self.agenda_groups.remove(self.agenda_groups[_group])
        self.write_down(self.agenda_groups)

    def do_add_group(self, _group):
        self.agenda_groups.append(_group)
        self.write_down(self.agenda_groups)

    def do_update_group(self, _old, _new):
        self.agenda_groups[_old] = _new
        self.write_down(self.agenda_groups)

    def menu_action(self, _action):

        if _action is 'print':
            for _group in self.agenda_groups:
                print(_group)

        elif _action is 'create':
            print("Insert Agenda-group name\n")
            _agenda = raw_input('Agenda-group: ')
            self.do_add_group(_agenda)

        elif _action is 'update':
            self.print_groups()
            print("Which Agenda-group do you want to update? \n")
            _choice = input('Please make a choice: ')
            _old = self.agenda_groups[_choice-1]
            print("Wat's the new value? (previous:{0})".format(_old))
            _new = raw_input('Please make a choice: ')
            self.do_update_group(_old,_new)

        elif _action is 'remove':
            self.print_groups()
            print("Which Agenda-group do you want to delete? \n")
            _choice = input('Please make a choice: ')
            self.do_delete_group(_choice-1)


    def show_menu(self):
        menu_text = """\nWhat would you like to do?
--------------------------
1) Print agenda-groups
2) Add agenda-group
3) Update agenda-group
4) Remove agenda-group
5) Exit\n"""
        while True:
            print(menu_text)
            try:
                # user input
                print("Please make a choice: ")
                choice = input()
                if choice == 1:
                    self.menu_action('print')
                elif choice == 2:
                    self.menu_action('create')
                elif choice == 3:
                    self.menu_action('update')
                elif choice == 4:
                    self.menu_action('remove')
                elif choice == 5:
                    break
                else:
                    raise Exception("Unavailable choice!")
            except Exception as e:
                print(e.message)
