__author__ = 'Giorgio Gambino'

import collections

_manager_actions = collections.defaultdict(dict)

def bind_action(_manager, _name):
    def _bind(_func):
        _m_name = _func.__name__
        _manager_actions[_manager][_name] = _m_name
        return _func
    return _bind

def get_actions(_manager):
    return _manager_actions[_manager]
