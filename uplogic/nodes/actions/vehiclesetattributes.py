from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met
from uplogic.physics import FWD
from uplogic.physics import RWD
from uplogic.physics import FOURWD


class ULVehicleSetAttributes(ULActionNode):
    def __init__(self, value_type=RWD):
        ULActionNode.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.vehicle = None
        self.wheelcount = None
        self.set_suspension_compression = False
        self.suspension_compression = False
        self.set_suspension_stiffness = False
        self.suspension_stiffness = False
        self.set_suspension_damping = False
        self.suspension_damping = False
        self.set_tyre_friction = False
        self.tyre_friction = False
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def set_attributes(self, vehicle, wheel, attrs, values):
        if attrs[0] is True:
            vehicle.set_wheel_suspension(wheel, values[0])
        if attrs[1] is True:
            vehicle.set_wheel_stiffness(wheel, values[1])
        if attrs[2] is True:
            vehicle.set_wheel_damping(wheel, values[2])
        if attrs[3] is True:
            vehicle.set_wheel_friction(wheel, values[3])

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        game_object = self.get_input(self.vehicle)
        value_type = self.get_input(self.value_type)
        wheelcount = self.get_input(self.wheelcount)
        if is_waiting(value_type, wheelcount):
            return
        if is_invalid(game_object):
            return
        attrs_to_set = [
            self.get_input(self.set_suspension_compression),
            self.get_input(self.set_suspension_stiffness),
            self.get_input(self.set_suspension_damping),
            self.get_input(self.set_tyre_friction)
        ]
        values_to_set = [
            self.get_input(self.suspension_compression),
            self.get_input(self.suspension_stiffness),
            self.get_input(self.suspension_damping),
            self.get_input(self.tyre_friction)
        ]
        vehicle = game_object.get('_vconst', None)
        if not vehicle:
            return
        self._set_ready()
        if value_type == FWD:
            for wheel in range(wheelcount):
                self.set_attributes(
                    vehicle,
                    wheel,
                    attrs_to_set,
                    values_to_set
                )
        if value_type == RWD:
            for wheel in range(wheelcount):
                wheel = vehicle.getNumWheels() - wheel - 1
                self.set_attributes(
                    vehicle,
                    wheel,
                    attrs_to_set,
                    values_to_set
                )
        if value_type == FOURWD:
            for wheel in range(vehicle.getNumWheels()):
                self.set_attributes(
                    vehicle,
                    wheel,
                    attrs_to_set,
                    values_to_set
                )
        self.done = True
