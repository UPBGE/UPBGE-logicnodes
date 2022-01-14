from bge import constraints
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULSetCharacterGravity(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.gravity = None
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
        gravity = self.get_input(self.gravity)
        if is_waiting(gravity):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        physics = constraints.getCharacter(game_object)
        if physics:
            physics.gravity = gravity
        else:
            game_object.gravity = gravity
        self.done = True
