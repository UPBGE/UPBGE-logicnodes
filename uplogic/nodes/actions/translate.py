from mathutils import Vector
from uplogic.nodes import ULActionNode
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULTranslate(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.moving_object = None
        self.local = None
        self.vect = None
        self.speed = None
        self._t = None
        self._old_values = None

    def evaluate(self):
        condition = self.get_input(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        moving_object = self.get_input(self.moving_object)
        vect = self.get_input(self.vect)
        dx = vect.x
        dy = vect.y
        dz = vect.z
        speed = self.get_input(self.speed)
        local = self.get_input(self.local)
        if is_waiting(
            vect,
            dx,
            dy,
            dz,
            speed,
            local
        ):
            return
        if is_invalid(moving_object):
            return
        self._set_ready()
        if dx is None:
            return
        if dy is None:
            return
        if dz is None:
            return
        if speed is None:
            return
        if local is None:
            return
        new_values = (moving_object, dx, dy, dz, speed, local)
        if new_values != self._old_values:
            start_pos = (
                moving_object.localPosition if
                local else moving_object.worldPosition
            )
            end_pos = Vector((
                start_pos.x + dx, start_pos.y + dy, start_pos.z + dz
            ))
            distance = (start_pos - end_pos).length
            time_to_destination = distance / speed
            t_speed = 1.0 / time_to_destination
            self._old_values = new_values
            self._start_pos = start_pos.copy()
            self._end_pos = end_pos.copy()
            self._d_pos = (end_pos - start_pos)
            self._t_speed = t_speed
            self._t = 0.0
        t = self._t
        dt = self._t_speed * self.network.time_per_frame
        t += dt
        if t >= 1.0:
            self._set_value(True)
            self._t = 0.0
            if local:
                moving_object.localPosition = self._end_pos.copy()
            else:
                moving_object.worldPosition = self._end_pos.copy()
        else:
            npos = self._start_pos + (self._d_pos * t)
            if local:
                moving_object.localPosition = npos
            else:
                moving_object.worldPosition = npos
            self._t = t
            self._set_value(False)
