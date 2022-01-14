from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULSetRigidBody(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.activate = False
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
        activate = self.get_input(self.activate)
        if is_waiting(game_object, activate):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        if activate:
            game_object.enableRigidBody()
        else:
            game_object.disableRigidBody()
        self.done = True
