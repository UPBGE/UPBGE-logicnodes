from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULApplyForce(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.force = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        game_object = self.get_input(self.game_object)
        force = self.get_input(self.force)
        local = self.local
        if is_waiting(force):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        game_object.applyForce(force, local)
        self.done = True
