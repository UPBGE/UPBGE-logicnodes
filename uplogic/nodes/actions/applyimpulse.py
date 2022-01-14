from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULApplyImpulse(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.point = None
        self.impulse = None
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
        point = self.get_input(self.point)
        impulse = self.get_input(self.impulse)
        local = self.local
        if hasattr(point, 'worldPosition'):
            point = point.worldPosition
        if is_waiting(point, impulse) or is_invalid(game_object):
            return
        self._set_ready()
        if impulse:
            game_object.applyImpulse(point, impulse, local)
        self.done = True
