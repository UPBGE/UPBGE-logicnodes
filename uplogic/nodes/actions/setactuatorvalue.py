from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULActionNode
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULSetActuatorValue(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_obj = None
        self.act_name = None
        self.field = None
        self.value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        game_obj = self.get_input(self.game_obj)
        act_name = self.get_input(self.act_name)
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        actuator = game_obj.actuators.get(act_name)
        if not actuator:
            return
        self._set_ready()
        field = self.get_input(self.field)
        value = self.get_input(self.value)
        if is_waiting(field, value):
            return
        setattr(actuator, field, value)
        self.done = True
