from uplogic.nodes import ULActionNode
from uplogic.utils import is_waiting
from uplogic.utils import not_met
from uplogic.utils import move_to


# Action "Move To": an object will follow a point
class ULMoveTo(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        # list of parameters of this action
        self.condition = None
        self.moving_object = None
        self.destination_point = None
        self.speed = None
        self.dynamic = None
        self.distance = None

    def evaluate(self):  # the actual execution of this cell
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        moving_object = self.get_input(self.moving_object)
        destination_point = self.get_input(self.destination_point)
        speed = self.get_input(self.speed)
        distance = self.get_input(self.distance)
        dynamic = self.get_input(self.dynamic)
        if hasattr(destination_point, 'worldPosition'):
            destination_point = destination_point.worldPosition
        if is_waiting(
            moving_object,
            destination_point,
            speed,
            distance,
            dynamic
        ):
            return
        self._set_ready()
        self._set_value(move_to(
            moving_object,
            destination_point,
            speed,
            self.network.time_per_frame,
            dynamic,
            distance
        ))
