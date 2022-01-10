from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULConditionNode
from uplogic.utils import STATUS_WAITING, is_invalid
from uplogic.utils import is_waiting


class ULSensorPositive(ULConditionNode):

    def __init__(self):
        ULConditionNode.__init__(self)
        self.obj_name = None
        self.sens_name = None
        self.OUT = ULOutSocket(self, self.get_sensor)

    def get_sensor(self):
        socket = self.get_output('sensor')
        if socket is None:
            game_obj = self.get_input(self.obj_name)
            sens_name = self.get_input(self.sens_name)
            if is_waiting(sens_name):
                return STATUS_WAITING
            if is_invalid(game_obj):
                return STATUS_WAITING
            if sens_name not in game_obj.sensors:
                return STATUS_WAITING
            return self.set_output(
                'sensor',
                game_obj.sensors[sens_name].positive
            )
        return socket

    def evaluate(self):
        self._set_ready()
