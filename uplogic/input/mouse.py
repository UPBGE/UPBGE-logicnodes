from bge import logic
from bge import events
from bge import render


MOUSE_EVENTS = logic.mouse.inputs
'''Reference to `bge.logic.mouse.inputs`
'''

LMB = events.LEFTMOUSE
RMB = events.RIGHTMOUSE
MMB = events.MIDDLEMOUSE


def set_mouse_position(x: int, y: int, absolute: bool = False):
    if absolute:
        render.setMousePosition(x, y)
        return
    render.setMousePosition(
        int(x * render.getWindowWidth()),
        int(y * render.getWindowHeight())
    )


def get_mouse_position(absolute: bool = False):
    pos = logic.mouse.position
    if absolute:
        return (
            int(pos[0] * render.getWindowWidth()),
            int(pos[1] * render.getWindowHeight())
        )
    return pos


def mouse_moved(tap: bool = False) -> bool:
    '''Detect mouse movement.

    :param tap: Only use the first consecutive `True` output

    :returns: boolean
    '''
    if tap:
        return (
            MOUSE_EVENTS[events.MOUSEX].activated or
            MOUSE_EVENTS[events.MOUSEY].activated
        )
    else:
        return (
            MOUSE_EVENTS[events.MOUSEX].active or
            MOUSE_EVENTS[events.MOUSEY].active or
            MOUSE_EVENTS[events.MOUSEX].activated or
            MOUSE_EVENTS[events.MOUSEY].activated
        )


def mouse_tap(button=events.LEFTMOUSE) -> bool:
    '''Detect mouse button tap.

    :param button: can be either `LMB`, `RMB` or `MMB` from `uplogic.input`

    :returns: boolean
    '''
    return (
        MOUSE_EVENTS[button].activated or
        MOUSE_EVENTS[button].activated
    )


def mouse_down(button=events.LEFTMOUSE) -> bool:
    '''Detect mouse button held down.

    :param button: can be either `LMB`, `RMB` or `MMB` from `uplogic.input`

    :returns: boolean
    '''
    return (
        MOUSE_EVENTS[button].active or
        MOUSE_EVENTS[button].activated or
        MOUSE_EVENTS[button].active or
        MOUSE_EVENTS[button].activated
    )


def mouse_up(button=events.LEFTMOUSE) -> bool:
    '''Detect mouse button released.

    :param button: can be either `LMB`, `RMB` or `MMB` from `uplogic.input`

    :returns: boolean
    '''
    return (
        MOUSE_EVENTS[button].released or
        MOUSE_EVENTS[button].released
    )


def mouse_wheel(tap: bool = False) -> int:
    '''Detect mouse wheel activity.

    :param tap: Only use the first consecutive `True` output

    :returns: -1 if wheel down, 0 if idle, 1 if wheel up
    '''
    if tap:
        return (
            MOUSE_EVENTS[events.WHEELUPMOUSE].activated -
            MOUSE_EVENTS[events.WHEELDOWNMOUSE].activated
        )
    else:
        return (
            (
                MOUSE_EVENTS[events.WHEELUPMOUSE].activated or
                MOUSE_EVENTS[events.WHEELUPMOUSE].active
            ) - (
                MOUSE_EVENTS[events.WHEELDOWNMOUSE].activated or
                MOUSE_EVENTS[events.WHEELDOWNMOUSE].active
            )
        )
