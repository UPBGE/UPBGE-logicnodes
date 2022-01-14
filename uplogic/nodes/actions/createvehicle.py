from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.physics.vehicle import ULVehicle
from uplogic.utils import VEHICLE
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULCreateVehicle(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.suspension = None
        self.stiffness = None
        self.damping = None
        self.friction = None
        self.wheel_size = None
        self.done = None
        self.vehicle = None
        self.wheels = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.VEHICLE = ULOutSocket(self, self.get_vehicle)
        self.WHEELS = ULOutSocket(self, self.get_wheels)

    def get_done(self):
        return self.done

    def get_vehicle(self):
        return self.vehicle

    def get_wheels(self):
        return self.wheels

    def evaluate(self):
        self.done = False
        game_object = self.get_input(self.game_object)
        if not_met(self.get_input(self.condition)):
            if game_object.get(VEHICLE):
                self._set_ready()
                self.vehicle = game_object[VEHICLE]
            return
        suspension = self.get_input(self.suspension)
        stiffness = self.get_input(self.stiffness)
        damping = self.get_input(self.damping)
        friction = self.get_input(self.friction)
        wheel_size = self.get_input(self.wheel_size)
        if is_waiting(
            game_object,
            suspension,
            stiffness,
            damping,
            friction,
            wheel_size
        ):
            return
        self._set_ready()
        self.vehicle = ULVehicle(
            game_object,
            suspension,
            stiffness,
            damping,
            friction,
            wheel_size
        )
        self.done = True
