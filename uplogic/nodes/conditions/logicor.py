from uplogic.nodes import ULConditionNode
from uplogic.utils import is_waiting


class ULOr(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.ca = False
        self.cb = False

    def evaluate(self):
        ca = self.get_input(self.ca)
        cb = self.get_input(self.cb)
        self._set_ready()
        if is_waiting(ca, cb):
            self._set_value(False)
        self._set_value(ca or cb)


class ULOrList(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.ca = False
        self.cb = False
        self.cc = False
        self.cd = False
        self.ce = False
        self.cf = False

    def evaluate(self):
        ca = self.get_input(self.ca)
        cb = self.get_input(self.cb)
        cc = self.get_input(self.cc)
        cd = self.get_input(self.cd)
        ce = self.get_input(self.ce)
        cf = self.get_input(self.cf)
        self._set_ready()
        if is_waiting(ca, cb, cc, cd, ce, cf):
            self._set_value(False)
        self._set_value(ca or cb or cc or cd or ce or cf)
