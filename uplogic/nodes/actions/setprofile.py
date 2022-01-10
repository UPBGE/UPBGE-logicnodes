from bge import render
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULSetProfile(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.use_profile = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        use_profile = self.get_input(self.use_profile)
        if is_waiting(use_profile):
            return
        self._set_ready()
        render.showProfile(use_profile)
        self.done = True
