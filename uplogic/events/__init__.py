'''TODO: Documentation
'''

from bge import logic
from uplogic.data.globaldb import GlobalDB


class ULEvent():
    '''TODO: Documentation
    '''

    def __init__(self, name: str, content=None, messenger=None):
        self.name = name
        self.content = content
        self.messenger = messenger
        self.scene = logic.getCurrentScene()
        self.scene.pre_draw.append(self.register)
        self.events = GlobalDB.retrieve('uplogic.events')

    def register(self, cam):
        self.events.put(self.name, [self.content, self.messenger, self])
        self.scene.pre_draw.remove(self.register)
        self.scene.pre_draw.append(self.unregister)

    def unregister(self):
        self.events.pop(self.name, None)
        self.scene.pre_draw.remove(self.unregister)


def throw(name: str, content=None, messenger=None) -> None:
    '''TODO: Documentation
    '''
    ULEvent(name, content, messenger)


def catch(name: str):
    '''TODO: Documentation
    '''
    events = GlobalDB.retrieve('uplogic.events')
    return events.pop(name, None)


def consume(name: str):
    '''TODO: Documentation
    '''
    events = GlobalDB.retrieve('uplogic.events')
    return events.pop(name)
