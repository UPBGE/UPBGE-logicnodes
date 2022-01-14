from uplogic.nodes import ULActionNode
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import not_met
from uplogic.utils import xrot_to
from uplogic.utils import yrot_to
from uplogic.utils import zrot_to


class ULRotateTo(ULActionNode):
    def __init__(self):
        self.condition = None
        self.moving_object = None
        self.target_point = None
        self.speed = None
        self.rot_axis = 2
        self.front_axis = 0

    def evaluate(self):
        self._set_value(False)
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        moving_object = self.get_input(self.moving_object)
        target_point = self.get_input(self.target_point)
        speed = self.get_input(self.speed)
        if hasattr(target_point, 'worldPosition'):
            target_point = target_point.worldPosition
        rot_axis = self.get_input(self.rot_axis)
        front_axis = self.get_input(self.front_axis)
        if is_invalid(moving_object):
            return
        if is_waiting(target_point, speed, rot_axis, front_axis):
            return
        self._set_ready()
        if rot_axis == 0:
            self._set_value(
                xrot_to(
                    moving_object,
                    target_point,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )
        elif rot_axis == 1:
            self._set_value(
                yrot_to(
                    moving_object,
                    target_point,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )
        elif rot_axis == 2:
            self._set_value(
                zrot_to(
                    moving_object,
                    target_point,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )
