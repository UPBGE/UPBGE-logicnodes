from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULSetVisibility(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.visible: bool = None
        self.recursive: bool = None
        self.done: bool = None
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
        visible: bool = self.get_input(self.visible)
        recursive: bool = self.get_input(self.recursive)
        if is_waiting(visible, recursive):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        if visible is None:
            return
        if recursive is None:
            return
        game_object.setVisible(visible, recursive)
        self.done = True
