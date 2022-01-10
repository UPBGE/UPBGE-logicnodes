from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULToggleProperty(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.property_name = None
        self.done = False
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_input(self.game_object)
        property_name = self.get_input(self.property_name)
        if is_waiting(property_name):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        if condition:
            value = game_object[property_name]
            game_object[property_name] = not value
        self.done = True
