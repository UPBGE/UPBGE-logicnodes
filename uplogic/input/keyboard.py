'''TODO: Documentation
'''

from bge import logic
from bge import events

keys_active = {}


def key_event(key):
    '''TODO: Documentation
    '''
    return logic.keyboard.inputs[getattr(events, f'{key}KEY')]


def key_tap(key):
    '''TODO: Documentation
    '''
    return key_event(key).activated


def key_down(key):
    '''TODO: Documentation
    '''
    return key_event(key).active


def key_pulse(key, time=.4):
    '''TODO: Documentation
    '''
    if key_event(key).activated:
        keys_active[key] = 0
        return True
    k = keys_active.get(key, 0)
    keys_active[key] = k + (1 / logic.getAverageFrameRate())
    if keys_active[key] > time:
        return key_event(key).active
    return False
