from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULApplyMovement(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.movement = None
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
        movement = self.get_input(self.movement)
        local = self.local
        if is_waiting(game_object, movement, local):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if movement:
            game_object.applyMovement(movement, local)
        self.done = True
