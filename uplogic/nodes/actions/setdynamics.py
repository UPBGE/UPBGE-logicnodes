from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULSetDynamics(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.activate = False
        self.ghost = None
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
        ghost = self.get_input(self.ghost)
        activate = self.get_input(self.activate)
        if is_waiting(game_object, ghost, activate):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if activate:
            game_object.restoreDynamics()
        else:
            game_object.suspendDynamics(ghost)
        self.done = True
