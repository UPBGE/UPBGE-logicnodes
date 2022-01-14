from bge import logic
from bge import events


KEYBOARD_EVENTS = logic.keyboard.inputs
'''Reference to `bge.logic.keyboard.inputs`
'''

_keys_active = {}


def key_event(key: str) -> bool:
    '''Retrieve key event.\n
    Not intended for manual use.
    '''
    return KEYBOARD_EVENTS[
        getattr(
            events, f'{key}KEY',
            (getattr(events, f'PAD{key}', None))
        )
    ]


def pad_event(key: str) -> bool:
    '''Retrieve Numpad event.\n
    Not intended for manual use.
    '''
    return KEYBOARD_EVENTS[getattr(events, f'PAD{key}')]


def key_tap(key: str) -> bool:
    '''Detect key tapped.

    :param key: key as `str` (e.g. `'A'`)

    :returns: boolean
    '''
    return key_event(key).activated


def key_down(key: str) -> bool:
    '''Detect key held down.

    :param key: key as `str` (e.g. `'A'`)

    :returns: boolean
    '''
    return key_event(key).active


def key_up(key: str) -> bool:
    '''Detect key released.

    :param key: key as `str` (e.g. `'A'`)

    :returns: boolean
    '''
    return key_event(key).released


def key_pulse(key: str, time: float = .4) -> bool:
    '''Detect key tapped, then held down after `time` has passed.

    :param key: key as `str` (e.g. `'A'`)
    :param time: timeout for key down

    :returns: boolean
    '''
    if key_event(key).activated:
        _keys_active[key] = 0
        return True
    k = _keys_active.get(key, 0)
    _keys_active[key] = k + (1 / logic.getAverageFrameRate())
    if _keys_active[key] > time:
        return key_event(key).active
    return False
