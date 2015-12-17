
import collections
from os import path
import string
from  rules import policies
from  rules.agendamanager import AgendaManager
import os
import re

class RuleManager():

    def __init__(self):
        self.rule_info_list = self.load_all_rules()
        self.agenda_manager = AgendaManager()
        
    def load_all_rules(self):
        _info_list = collections.defaultdict(dict)
        _policy_files = self.load_policy_files()
        for _policy in _policy_files:
            _policy_info = self.load_rule_info(_policy)
            for _key,_val in _policy_info.iteritems():
                _info_list[_policy][_key] = _val
        return _info_list

    def load_rule_info(self, _name):
        _info_line = re.compile(r'^\S+\=\S+$')
        _numeric = re.compile(r'^\d+(\.\d*)?$')
        _ruleFile = open( policies.__path__[0] + '/' + _name, 'r')
        _rule_info = { }

        for _line in _ruleFile:
            if _info_line.match(_line):
                _tokens = _line.rstrip().split('=')
                _rule_info[_tokens[0]] = _tokens[1][1:-1] if not _numeric.match(_tokens[1]) else _tokens[1]

        _ruleFile.close()

        return _rule_info

    def load_policy_files(self):
        def is_policy(_file):
            return _file.endswith('.policy')

        _rules = filter(is_policy, os.listdir( policies.__path__[0]))
        return _rules

    def print_policy_files(self):
        i = 1
        for _policy,_ in self.rule_info_list.iteritems():
            print("{0}) {1}".format(i,_policy[0:-7]))
            i += 1

    def write_down(self, _rule_vars, _mode='create'):
        _section = re.compile(r'^\[\w+\]$')
        _numeric = re.compile(r'^\d+(\.\d*)?$')
        _skel = { }
        _File = open('./rules/skel/template.policy', 'r')
        _OFile = open( policies.__path__[0] + '/' + _rule_vars['rule_name'] +  '.policy', 'a')
        if _mode is 'update':
            _OFile.seek(0)
            _OFile.truncate()

        _sect = ''
        for _line in _File:
            if _section.match(_line):
                _skel[_line[1:-2]] = [ ]
                _sect = _line[1:-2]
            else:
                _skel[_sect].append(_line[0:-1])
        _File.close()

        _OFile.write("## Policy generated from Rulemanager ##\n\n")
        _OFile.write("## Import Statements ##\n\n")

        for _line in _skel['imports']:
            _OFile.write(_line + '\n')
        """
        _rule_vars = {
            'rule_name' : name,
            'rule_agenda' : 'cpu',
            'rule_metric' : 'CPU',
            'rule_threshold' : '0.2',
            'rule_operator' : 'tope',
            'rule_action' : 'alarm',
            }
        """
        _OFile.write("\n## Rule Parameters ##\n")
        for _var_key, _var_val in _rule_vars.iteritems():
            for _line  in _skel['rule_params']:
                if _var_key in _line:
                    if _numeric.match(_var_val):
                        _newline = _line + _var_val
                    else:
                        _newline = _line + '"' + _var_val + '"'
                    _OFile.write(_newline + '\n')

        _OFile.write("\n## Rule Body ##\n")
        for _line  in _skel['rule_body']:
            if 'NAME' in _line:
                _newline = re.sub('NAME', 'rule_name', _line)
                _OFile.write(_newline + '\n')
            elif 'AGENDA' in _line:
                _newline = re.sub('AGENDA', 'agenda-group ' + _rule_vars['rule_agenda'], _line)
                _OFile.write(_newline + '\n')
            elif 'WHEN' in _line:
                if _rule_vars['rule_operator'] == 'tope':
                    _operator = '>='
                _newline=re.sub('WHEN', '$resource := Resource( get_sample(get_metric(rule_metric,MetaManager.get_current()))'+ _operator + 'rule_threshold )', _line)
                _OFile.write(_newline + '\n')
            elif 'ACTION' in _line:
                _newline = re.sub('ACTION', '$resource.action(rule_action)', _line)
                _OFile.write(_newline + '\n')
            else:
                _OFile.write(_line + '\n')
        _OFile.close()

    def do_delete_rule(self, _rule):
        os.remove( policies.__path__[0] + '/' + _rule)
        self.rule_info_list = self.load_all_rules()

    def print_rules(self):
        print('#### Rules ####\n')
        print("%s %s %s %s %s" % ("|Name|", "Agenda|", "Metric|", "Threshold|","Operator|"))
        for _, _rule in self.rule_info_list.iteritems():
            print('|{0}| {1}| {2}| {3}| {4}|'.format(_rule['rule_name'],_rule['rule_agenda'],_rule['rule_metric'],_rule['rule_threshold'],_rule['rule_operator'], ))

    def menu_action(self,_action):

        if _action is 'remove':
            self.print_policy_files()
            print("Which policy do you want to delete?\n")
            choice = input('Please make a choice: ')
            self.do_delete_rule(self.rule_info_list.keys()[choice-1])

        elif _action is 'create':
            _rule_params = { }

            print("Insert policy name\n")
            _name = raw_input('name: ')
            _rule_params['rule_name'] = _name

            print("Insert Agenda-group name\n")
            _agenda = raw_input('Agenda-group: ')
            _rule_params['rule_agenda'] = _agenda

            print("Insert metric name\n")
            _metric = raw_input('metric: ')
            _rule_params['rule_metric'] = _metric

            print("Insert threshold\n")
            _threshold = raw_input('threshold: ')
            _rule_params['rule_threshold'] = _threshold

            print("Insert operator\n")
            _operator = raw_input('operator: ')
            _rule_params['rule_operator'] = _operator

            print("Insert action\n")
            _action = raw_input('action: ')
            _rule_params['rule_action'] = _action

            self.write_down(_rule_params)
            #del self.rule_info_list
            self.rule_info_list = self.load_all_rules()

        elif _action is 'update':
            self.print_policy_files()
            print("Which policy do you want to modify?\n")
            choice = input('Please make a choice: ')
            _rule_params = self.load_rule_info(self.rule_info_list.keys()[choice-1])

            print("Insert Agenda-group name\n")
            _agenda = raw_input('Agenda-group: (current: {0})\n'.format(_rule_params['rule_agenda']))
            if _agenda:
                _rule_params['rule_agenda'] = _agenda

            print("Insert metric name\n")
            _metric = raw_input('metric: (current: {0})\n'.format(_rule_params['rule_metric']))
            if _metric:
                _rule_params['rule_metric'] = _metric

            print("Insert threshold\n")
            _threshold = raw_input('threshold: (current: {0})\n'.format(_rule_params['rule_threshold']))
            if _threshold:
                _rule_params['rule_threshold'] = _threshold

            print("Insert operator\n")
            _operator = raw_input('operator: (current: {0})\n'.format(_rule_params['rule_operator']))
            if _operator:
                _rule_params['rule_operator'] = _operator

            print("Insert action\n")
            _action = raw_input('action: (current: {0})\n'.format(_rule_params['rule_action']))
            if _action:
                _rule_params['rule_action'] = _action

            self.write_down(_rule_params,'update')
            self.rule_info_list = self.load_all_rules()

        elif _action is 'print':
            self.print_rules()

    def show_menu(self):
        menu_text = """\nWhat would you like to do?
--------------------------
1) Print rules
2) Create rule
3) Modify rule
4) Delete rule
5) Manage agenda-groups
6) Exit\n"""
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
                    self.agenda_manager.show_menu()
                elif choice == 6:
                    break
                else:
                    raise Exception("Unavailable choice!")
            except Exception as e:
                print(e.message)
