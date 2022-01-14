from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULSetDictKey(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.dict = None
        self.key = None
        self.val = None
        self.new_dict = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.DICT = ULOutSocket(self, self.get_dict)

    def get_done(self):
        return self.done

    def get_dict(self):
        return self.new_dict

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        dictionary = self.get_input(self.dict)
        key = self.get_input(self.key)
        val = self.get_input(self.val)
        if is_waiting(dictionary, key, val):
            return
        self._set_ready()
        dictionary[key] = val
        self.new_dict = dictionary
        self.done = True
