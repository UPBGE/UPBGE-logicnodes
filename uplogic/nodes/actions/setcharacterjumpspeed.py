from bge import constraints
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULSetCharacterJumpSpeed(ULActionNode):
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
            self._set_ready()
            return
        game_object = self.get_input(self.game_object)
        force = self.get_input(self.force)
        if is_waiting(game_object):
            return
        physics = constraints.getCharacter(game_object)
        self._set_ready()
        if is_invalid(game_object):
            return
        physics.jumpSpeed = force
        self.done = True
