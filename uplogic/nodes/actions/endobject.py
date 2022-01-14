from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULEndObject(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.scene = None
        self.game_object = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        game_object = self.get_input(self.game_object)
        if not_met(condition):
            return
        if is_waiting(game_object):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if game_object is self.network._owner:
            self.network._do_remove = True
        game_object.endObject()
        self.done = True
