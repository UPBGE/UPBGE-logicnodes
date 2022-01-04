from math import pi
from bge import logic
from mathutils import Vector
from uplogic.utils import clamp
from uplogic.utils import raycast


class ULShip():

    def __init__(self, ship, buoyancy=1, height=100) -> None:
        self.ship = ship
        self.height = height
        cs = sorted(ship.childrenRecursive, key=lambda c: c.name)
        self.buoys = [c for c in cs if 'Buoy' in c.name]
        self.buoyancy = buoyancy
        logic.getCurrentScene().pre_draw.append(self.update)

    def update(self):
        up = Vector((0, 0, 1))
        lifts = len(self.buoys)
        ship = self.ship
        lindamp = .1
        for buoy in self.buoys:
            wpos = buoy.worldPosition
            obj, point, normal, direction = raycast(buoy, wpos, up, self.height, 'water', True, True)
            if obj:
                lindamp += (.7 / lifts)
                lift = (up * (wpos - point).length * self.buoyancy) / lifts
                ship.applyImpulse(
                    wpos,
                    clamp(lift, max=10),
                    False
                )
        ship.linearDamping = lindamp
        ship.angularDamping = lindamp / 2

    def destroy(self):
        logic.getCurrentScene().pre_draw.remove(self.update)
