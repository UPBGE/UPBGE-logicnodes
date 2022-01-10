from bge import logic
from bge import render
from mathutils import Vector
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULProjectileRayCast(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.origin = None
        self.destination = None
        self.power: float = None
        self.resolution: float = None
        self.property_name: str = None
        self.xray: bool = None
        self.distance: float = None
        self.visualize: bool = None
        self._picked_object = None
        self._point = None
        self._normal = None
        self._parabola = None
        self.PICKED_OBJECT = ULOutSocket(self, self.get_picked_object)
        self.POINT = ULOutSocket(self, self.get_point)
        self.NORMAL = ULOutSocket(self, self.get_normal)
        self.PARABOLA = ULOutSocket(self, self.get_parabola)
        self.network = None

    def setup(self, network):
        self.network = network

    def get_picked_object(self):
        return self._picked_object

    def get_parabola(self):
        return self._parabola

    def get_point(self):
        return self._point

    def get_normal(self):
        return self._normal

    def calc_projectile(self, t, vel, pos):
        half: float = logic.getCurrentScene().gravity.z * (.5 * t * t)
        vel = vel * t
        return Vector((0, 0, half)) + vel + pos

    def evaluate(self):
        condition = self.get_input(self.condition)
        if not_met(condition):
            self._set_value(False)
            self._out_normal = None
            self._out_object = None
            self._out_point = None
            return
        origin = self.get_input(self.origin)
        power: float = self.get_input(self.power)
        destination = self.get_input(self.destination)
        resolution: float = 1 - (self.get_input(self.resolution) * .99)
        property_name: str = self.get_input(self.property_name)
        xray: bool = self.get_input(self.xray)
        distance: float = self.get_input(self.distance)
        visualize: bool = self.get_input(self.visualize)

        if is_waiting(origin, destination, property_name, distance):
            return
        destination.normalize()
        destination *= power
        origin = getattr(origin, 'worldPosition', origin)

        points: list = []
        color: list = [1, 0, 0]
        idx = 0
        total_dist: float = 0
        found: bool = False
        owner = self.network._owner

        self._set_ready()

        while total_dist < distance:
            target = (self.calc_projectile(idx, destination, origin))
            start = origin if not points else points[-1]
            obj, point, normal = owner.rayCast(
                start,
                target,
                prop=property_name,
                xray=xray
            )
            total_dist += (target-start).length
            if not obj:
                points.append(target)
            else:
                points.append(point)
                color = [0, 1, 0]
                found = True
                break
            idx += resolution
        if visualize:
            for i, p in enumerate(points):
                if i < len(points) - 1:
                    render.drawLine(p, points[i+1], color)
        self._set_value(points[-1] if found else None)
        self._picked_object = obj
        self._point = point
        self._normal = normal
        self._parabola = points
