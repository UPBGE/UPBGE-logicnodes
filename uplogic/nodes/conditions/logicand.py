from uplogic.nodes import ULConditionNode
from uplogic.utils import is_waiting


class ULAnd(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.ca = None
        self.cb = None

    def evaluate(self):
        ca = self.get_input(self.ca)
        cb = self.get_input(self.cb)
        self._set_ready()
        if is_waiting(ca, cb):
            self._set_value(False)
            return
        self._set_value(ca and cb)


class ULAndList(ULConditionNode):

    def __init__(self):
        ULConditionNode.__init__(self)
        self.ca = True
        self.cb = True
        self.cc = True
        self.cd = True
        self.ce = True
        self.cf = True

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
            return
        self._set_value(ca and cb and cc and cd and ce and cf)
