from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULGetActuatorValue(ULParameterNode):

    def __init__(self):
        ULParameterNode.__init__(self)
        self.game_obj = None
        self.act_name = None
        self.field = None
        self.OUT = ULOutSocket(self, self.get_actuator)

    def get_actuator(self):
        socket = self.get_output('actuator')
        if socket is None:
            game_obj = self.get_input(self.game_obj)
            act_name = self.get_input(self.act_name)
            field = self.get_input(self.field)
            if is_invalid(game_obj, act_name, field):
                return STATUS_WAITING
            if act_name not in game_obj.actuators:
                return STATUS_WAITING
            return self.set_output(
                'actuator',
                getattr(game_obj.actuators[act_name], field)
            )
        return socket

    def evaluate(self):
        self._set_ready()
