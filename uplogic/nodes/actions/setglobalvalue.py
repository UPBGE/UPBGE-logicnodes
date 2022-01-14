from uplogic.data import GlobalDB
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULSetGlobalValue(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.data_id = None
        self.key = None
        self.value = None
        self.persistent = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        data_id = self.get_input(self.data_id)
        persistent = self.get_input(self.persistent)
        key = self.get_input(self.key)
        value = self.get_input(self.value)
        if is_waiting(data_id, persistent, key, value):
            return
        self._set_ready()
        if self.condition is None or condition:
            if data_id is None:
                return
            if persistent is None:
                return
            if key is None:
                return
            db = GlobalDB.retrieve(data_id)
            db.put(key, value, persistent)
            if self.condition is None:
                self.deactivate()
        self.done = True
