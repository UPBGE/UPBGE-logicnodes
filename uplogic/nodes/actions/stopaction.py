from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULStopAction(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.action_layer = None
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
        game_object = self.get_input(self.game_object)
        action_layer = self.get_input(self.action_layer)
        if is_waiting(game_object, action_layer):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if is_invalid(action_layer):
            return
        game_object.stopAction(action_layer)
        self.done = True
