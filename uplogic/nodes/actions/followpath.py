from mathutils import Vector
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import not_met
from uplogic.utils import rot_to
from uplogic.utils import move_to


class ULFollowPath(ULActionNode):
    class MotionPath(object):
        def __init__(self):
            self.points = []
            self.cursor = 0
            self.loop = False
            self.loop_start = 0

        def next_point(self):
            if self.cursor < len(self.points):
                return self.points[self.cursor]
            else:
                return None

        def advance(self):
            self.cursor += 1
            if self.cursor < len(self.points):
                return True
            else:
                if self.loop:
                    self.cursor = self.loop_start
                    return True
                return False

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.moving_object = None
        self.rotating_object = None
        self.path_points = None
        self.loop = None
        self.path_continue = None
        self.navmesh_object = None
        self.move_dynamic = None
        self.linear_speed = None
        self.reach_threshold = None
        self.look_at = None
        self.rot_speed = None
        self.rot_axis = None
        self.front_axis = None
        self._motion_path = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        path_continue = self.get_input(self.path_continue)
        if not_met(condition):
            if not path_continue:
                self._motion_path = None
            self._set_ready()
            return
        moving_object = self.get_input(self.moving_object)
        rotating_object = self.get_input(self.rotating_object)
        path_points = self.get_input(self.path_points)
        navmesh_object = self.get_input(self.navmesh_object)
        move_dynamic = self.get_input(self.move_dynamic)
        linear_speed = self.get_input(self.linear_speed)
        reach_threshold = self.get_input(self.reach_threshold)
        look_at = self.get_input(self.look_at)
        rot_axis = self.get_input(self.rot_axis)
        front_axis = self.get_input(self.front_axis)
        rot_speed = self.get_input(self.rot_speed)
        loop = self.get_input(self.loop)
        if is_invalid(
            path_points,
            move_dynamic,
            linear_speed,
            reach_threshold,
            look_at,
            rot_axis,
            front_axis,
            loop
        ):
            return
        if is_invalid(rot_speed):
            rot_speed = 0
        if loop is None:
            return
        if is_invalid(moving_object):
            return
        if is_invalid(navmesh_object):
            navmesh_object = None
        self._set_ready()
        self._set_value(False)
        if (self._motion_path is None) or (self._motion_path.loop != loop):
            self.generate_path(
                moving_object.worldPosition,
                path_points,
                navmesh_object,
                loop
            )
        next_point = self._motion_path.next_point()
        if next_point:
            tpf = self.network.time_per_frame
            if look_at:
                rot_to(
                    rot_axis,
                    rotating_object,
                    next_point,
                    front_axis,
                    rot_speed,
                    tpf
                )
            reached = move_to(
                moving_object,
                next_point,
                linear_speed,
                tpf,
                move_dynamic,
                reach_threshold
            )
            if reached:
                has_more = self._motion_path.advance()
                if not has_more:
                    self._set_value(True)
                    self.done = True

    def generate_path(self, start_position, path_points, navmesh_object, loop):
        if not path_points:
            return self._motion_path.points.clear()
        path = ULFollowPath.MotionPath()
        path.loop = loop
        points = path.points
        self._motion_path = path
        if not navmesh_object:
            points.append(Vector(start_position))
            if loop:
                path.loop_start = 1
            for p in path_points:
                points.append(Vector(p))
        else:
            last = path_points[-1]
            mark_loop_position = loop
            for p in path_points:
                subpath = navmesh_object.findPath(
                    start_position,
                    Vector(p)
                )
                if p is last:
                    points.extend(subpath)
                else:
                    points.extend(subpath[:-1])
                if mark_loop_position:
                    path.loop_start = len(points)
                    mark_loop_position = False
                start_position = Vector(p)
            if loop:
                subpath = navmesh_object.findPath(
                    Vector(last),
                    Vector(path_points[0])
                )
                points.extend(subpath[1:])
