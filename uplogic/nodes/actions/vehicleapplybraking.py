from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.physics import RWD
from uplogic.utils import VEHICLE
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULVehicleApplyBraking(ULActionNode):
    def __init__(self, value_type=RWD):
        ULActionNode.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.vehicle = None
        self.wheelcount = None
        self._reset = False
        self.power = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        game_object = self.get_input(self.vehicle)
        if is_invalid(game_object):
            return
        vehicle = game_object.get(VEHICLE, None)
        if vehicle is None:
            return
        value_type = self.get_input(self.value_type)
        wheelcount = self.get_input(self.wheelcount)
        power = self.get_input(self.power)
        if is_waiting(value_type, wheelcount, power):
            return
        self._set_ready()
        vehicle.brake(power, value_type, wheelcount)
        self.done = True
