'''TODO: Documentation
'''

from bge import logic
from uplogic.data.globaldb import GlobalDB


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
        events.lock(name)
        logic.getCurrentScene().pre_draw.append(self.register)

    def register(self, cam):
        scene = logic.getCurrentScene()
        if self.register not in scene.pre_draw:
            return
        if self.events.get(self.name):
            return
        self.events.unlock(self.name)
        scene.pre_draw.remove(self.register)
        self.events.put(self.name, self)
        scene.pre_draw.append(self.unregister)

    def unregister(self):
        if not self.events:
            return
        scene = logic.getCurrentScene()
        self.events.pop(self.name)
        scene.pre_draw.remove(self.unregister)


def throw(name: str, content=None, messenger=None) -> None:
    '''TODO: Documentation
    '''
    events = GlobalDB.retrieve('uplogic.events')
    if name not in events.locked:
        ULEvent(name, content, messenger, events)


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
