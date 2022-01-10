from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
from bge.types import KX_GameObject as GameObject


class ULGetSensorValue(ULParameterNode):

    def __init__(self):
        ULParameterNode.__init__(self)
        self.game_obj = None
        self.sens_name = None
        self.field = None
        self.OUT = ULOutSocket(self, self.get_sensor)

    def get_sensor(self):
        game_obj: GameObject = self.get_input(self.game_obj)
        sens_name: str = self.get_input(self.sens_name)
        field = self.get_input(self.field)
        if is_invalid(game_obj, sens_name, field):
            return STATUS_WAITING
        if sens_name not in game_obj.sensors:
            return STATUS_WAITING
        return getattr(game_obj.sensors[sens_name], field)

    def evaluate(self):
        self._set_ready()
