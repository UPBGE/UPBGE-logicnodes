from bge import render
from mathutils import Vector
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULRaycast(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.origin = None
        self.destination = None
        self.local: bool = None
        self.property_name: str = None
        self.xray: bool = None
        self.custom_dist: bool = None
        self.distance: float = None
        self.visualize: bool = None
        self._picked_object = None
        self._point = None
        self._normal = None
        self._direction = None
        self.PICKED_OBJECT = ULOutSocket(self, self.get_picked_object)
        self.POINT = ULOutSocket(self, self.get_point)
        self.NORMAL = ULOutSocket(self, self.get_normal)
        self.DIRECTION = ULOutSocket(self, self.get_direction)
        self.network = None

    def setup(self, network):
        self.network = network

    def get_picked_object(self):
        return self._picked_object

    def get_point(self):
        return self._point

    def get_normal(self):
        return self._normal

    def get_direction(self):
        return self._direction

    def _compute_direction(self, origin, dest, local, dist):
        custom_dist = self.get_input(self.custom_dist)
        start = (
            origin.worldPosition.copy()
            if hasattr(origin, "worldPosition")
            else origin
        )
        if hasattr(dest, "worldPosition"):
            dest = dest.worldPosition.copy()
        if local:
            dest = start + dest
        d = dest - start
        d.normalize()
        return d, dist if custom_dist else (start - dest).length, dest

    def evaluate(self):
        condition = self.get_input(self.condition)
        if not_met(condition):
            self._set_value(False)
            self._normal = None
            self._object = None
            return
        origin = self.get_input(self.origin)
        destination = self.get_input(self.destination)
        local: bool = self.get_input(self.local)
        property_name: str = self.get_input(self.property_name)
        xray: bool = self.get_input(self.xray)
        distance: float = self.get_input(self.distance)
        visualize: bool = self.get_input(self.visualize)

        if is_waiting(origin, destination, local, property_name, distance):
            return
        self._set_ready()
        caster = self.network._owner
        obj, point, normal = None, None, None
        direction, distance, destination = self._compute_direction(
            origin,
            destination,
            local,
            distance
        )
        if not property_name:
            obj, point, normal = caster.rayCast(
                destination,
                origin,
                distance,
                xray=xray
            )
        else:
            obj, point, normal = caster.rayCast(
                destination,
                origin,
                distance,
                property_name,
                xray=xray
            )
        if visualize:
            origin = getattr(origin, 'worldPosition', origin)
            line_dest: Vector = direction.copy()
            line_dest.x *= distance
            line_dest.y *= distance
            line_dest.z *= distance
            line_dest = line_dest + origin
            render.drawLine(
                origin,
                line_dest,
                [
                    1,
                    0,
                    0,
                    1
                ]
            )
            if obj:
                render.drawLine(
                    origin,
                    point,
                    [
                        0,
                        1,
                        0,
                        1
                    ]
                )
        self._set_value(obj is not None)
        self._picked_object = obj
        self._point = point
        self._normal = normal
        self._direction = direction
