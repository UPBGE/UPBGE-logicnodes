from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import debug
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULRemoveListIndex(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.items = None
        self.idx = None
        self.new_list = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.LIST = ULOutSocket(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.new_list

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        list_d = self.get_input(self.items)
        idx = self.get_input(self.idx)
        if is_invalid(list_d, idx):
            return
        self._set_ready()
        if len(list_d) > idx:
            del list_d[idx]
        else:
            debug("List Index exceeds length!")
            return
        self.new_list = list_d
        self.done = True
