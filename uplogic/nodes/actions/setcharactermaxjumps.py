from bge import constraints
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULSetCharacterMaxJumps(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.max_jumps = None
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
        max_jumps = self.get_input(self.max_jumps)
        if is_waiting(game_object, max_jumps):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        physics = constraints.getCharacter(game_object)
        physics.maxJumps = max_jumps
        self.done = True
