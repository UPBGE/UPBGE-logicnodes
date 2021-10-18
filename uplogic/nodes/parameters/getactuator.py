from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULGetActuator(ULParameterNode):

    def __init__(self):
        ULParameterNode.__init__(self)
        self.game_obj = None
        self.act_name = None
        self.OUT = ULOutSocket(self, self.get_actuator)

    def get_actuator(self):
        game_obj = self.get_socket_value(self.game_obj)
        act_name = self.get_socket_value(self.act_name)
        if is_invalid(game_obj, act_name):
            return STATUS_WAITING
        if act_name not in game_obj.actuators:
            return STATUS_WAITING
        return game_obj.actuators[act_name]

    def evaluate(self):
        self._set_ready()
