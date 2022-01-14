from bge import render
from uplogic.nodes import ULActionNode
from uplogic.utils import is_invalid
from uplogic.utils import not_met
from uplogic.utils import rot_to
from uplogic.utils import move_to


class ULMoveToWithNavmesh(ULActionNode):

    class MotionPath(object):
        def __init__(self):
            self.points = []
            self.cursor = 0
            self.destination = None

        def next_point(self):
            if self.cursor < len(self.points):
                return self.points[self.cursor]
            else:
                return None

        def destination_changed(self, new_destination):
            return self.destination != new_destination

        def advance(self):
            self.cursor += 1
            return self.cursor < len(self.points)

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.moving_object = None
        self.rotating_object = None
        self.navmesh_object = None
        self.destination_point = None
        self.move_dynamic = None
        self.linear_speed = None
        self.reach_threshold = None
        self.look_at = None
        self.rot_axis = None
        self.front_axis = None
        self.rot_speed = None
        self.visualize = None
        self._motion_path = None

    def evaluate(self):
        condition = self.get_input(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        moving_object = self.get_input(self.moving_object)
        rotating_object = self.get_input(self.rotating_object)
        navmesh_object = self.get_input(self.navmesh_object)
        destination_point = self.get_input(self.destination_point)
        move_dynamic = self.get_input(self.move_dynamic)
        linear_speed = self.get_input(self.linear_speed)
        reach_threshold = self.get_input(self.reach_threshold)
        look_at = self.get_input(self.look_at)
        rot_axis = self.get_input(self.rot_axis)
        front_axis = self.get_input(self.front_axis)
        rot_speed = self.get_input(self.rot_speed)
        visualize = self.get_input(self.visualize)
        if is_invalid(
            destination_point,
            move_dynamic,
            linear_speed,
            reach_threshold,
            look_at,
            rot_axis,
            front_axis,
            rot_speed,
            visualize
        ):
            return
        if is_invalid(moving_object, navmesh_object):
            return
        if is_invalid(rotating_object):
            rotating_object = None
        self._set_ready()
        if (
            (self._motion_path is None) or
            (self._motion_path.destination_changed(destination_point))
        ):
            points = navmesh_object.findPath(
                moving_object.worldPosition,
                destination_point
            )
            motion_path = ULMoveToWithNavmesh.MotionPath()
            motion_path.points = points[1:]
            motion_path.destination = destination_point
            self._motion_path = motion_path
        next_point = self._motion_path.next_point()
        if visualize:
            points = [moving_object.worldPosition.copy()]
            points.extend(self._motion_path.points[self._motion_path.cursor:])
            points.append(self._motion_path.destination)
            for i, p in enumerate(points):
                if i < len(points) - 1:
                    render.drawLine(
                        p, points[i + 1], [1, 0, 0, 1]
                    )
        if next_point:
            tpf = self.network.time_per_frame
            if look_at and (rotating_object is not None):
                rot_to(
                    rot_axis,
                    rotating_object,
                    next_point,
                    front_axis,
                    rot_speed,
                    tpf
                )
            ths = reach_threshold  # if next_point == self._motion_path.destination else .1  # noqa
            reached = move_to(
                moving_object,
                next_point,
                linear_speed,
                tpf,
                move_dynamic,
                ths
            )
            if reached:
                has_more = self._motion_path.advance()
                if not has_more:
                    self._set_value(True)
