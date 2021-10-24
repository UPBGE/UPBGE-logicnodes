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
    events = None
    name = ''
    content = None
    messenger = None

    def __init__(self, name, content=None, messenger=None, events=None):
        self.name = name
        self.content = content
        self.messenger = messenger
        self.events = GlobalDB.retrieve('uplogic.events')
        logic.getCurrentScene().pre_draw.append(self.register)

    def register(self, cam):
        scene = logic.getCurrentScene()
        if not self.register in scene.pre_draw:
            return
        scene.pre_draw.remove(self.register)
        self.events.put(self.name, self)
        scene.pre_draw.append(self.unregister)

    def unregister(self):
        if not self.events:
            return
        scene = logic.getCurrentScene()
        # self.events.log()
        self.events.pop(self.name)
        scene.pre_draw.remove(self.unregister)
        # self.events.log()
        # print('All Done')


def throw(name: str, content=None, messenger=None) -> None:
    '''TODO: Documentation
    '''
    ULEvent(name, content, messenger)


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
