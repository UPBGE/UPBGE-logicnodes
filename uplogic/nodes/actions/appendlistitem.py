from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULAppendListItem(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.items: list = None
        self.val = None
        self.new_list: list = None
        self.done: bool = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.LIST = ULOutSocket(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.new_list

    def evaluate(self):
        self.done: bool = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        list_d: list = self.get_input(self.items)
        val = self.get_input(self.val)
        if is_waiting(list_d, val):
            return
        self._set_ready()
        list_d.append(val)
        self.new_list = list_d
        self.done = True
