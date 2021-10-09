from uplogic.nodes import ULParameterNode
from uplogic.utils import is_invalid


class GetActuator(ULParameterNode):

    def __init__(self):
        ULParameterNode.__init__(self)
        self.obj_name = None
        self.act_name = None

    def evaluate(self):
        game_obj = self.get_socket_value(self.obj_name)
        if is_invalid(game_obj, self.act_name):
            return
        self._set_ready()
        self._set_value(game_obj.actuators[self.act_name])
