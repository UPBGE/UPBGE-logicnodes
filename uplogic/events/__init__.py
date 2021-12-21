'''TODO: Documentation
'''

from bge import logic
from uplogic.data.globaldb import GlobalDB
import time


class ULEventManager():
    events = {}

    def __init__(self):
        pass

    def register(name, content, messenger, events):
        pass


class ULEvent():
    '''TODO: Documentation
    '''

    def __init__(self, name, content=None, messenger=None, events=None):
        self.name = name
        self.content = content
        self.messenger = messenger
        self.events = events
        # self.events.lock(self.name, self)
        logic.getCurrentScene().pre_draw.append(self.register)

    def register(self, cam):
        scene = logic.getCurrentScene()
        if self.register not in scene.pre_draw:
            return
        if self.events.get(self.name):
            return
        # # self.events.unlock(self.name)
        self.events.put(self.name, self)
        scene.pre_draw.remove(self.register)
        scene.pre_draw_setup.append(self.unregister)

    def unregister(self):
        if not self.events:
            return
        scene = logic.getCurrentScene()
        self.events.pop(self.name)
        scene.pre_draw_setup.remove(self.unregister)


def throw(name: str, content=None, messenger=None) -> None:
    '''TODO: Documentation
    '''
    events = GlobalDB.retrieve('uplogic.events')
    ULEvent(name, content, messenger, events)
    # if name not in events.locked:
    # else:
    #     print(name, 'locked')


def catch(name: str):
    '''TODO: Documentation
    '''
    events = GlobalDB.retrieve('uplogic.events')
    return events.get(name)


def consume(name: str):
    '''TODO: Documentation
    '''
    events = GlobalDB.retrieve('uplogic.events')
    return events.pop(name)


def schedule(name: str, content=None, messenger=None, delay=0.0):
    ScheduledEvent(delay, name, content, messenger)


class ScheduledEvent():

    def __init__(self, delay, name, content, messenger):
        self.time = time.time()
        self.delay = self.time + delay
        self.name = name
        self.content = content
        self.messenger = messenger
        scene = self.scene = logic.getCurrentScene()
        scene.pre_draw.append(self.throw_scheduled)

    def throw_scheduled(self):
        if time.time() >= self.delay:
            self.scene.pre_draw.remove(self.throw_scheduled)
            events = GlobalDB.retrieve('uplogic.events')
            if self.name not in events.locked:
                ULEvent(self.name, self.content, self.messenger, events)


def schedule_callback(cb, delay=0.0, arg=None):
    ScheduledCallback(cb, delay, arg)


class ScheduledCallback():

    def __init__(self, cb, delay=0.0, arg=None):
        self.time = time.time()
        self.delay = self.time + delay
        self.callback = cb
        self.arg = arg
        scene = self.scene = logic.getCurrentScene()
        scene.pre_draw.append(self.call_scheduled)

    def call_scheduled(self):
        if time.time() >= self.delay:
            self.scene.pre_draw.remove(self.call_scheduled)
            if self.arg:
                self.callback(self.arg)
            else:
                self.callback()
