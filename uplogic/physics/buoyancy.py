from bge import logic
from mathutils import Vector
from uplogic.utils import vec_clamp
from uplogic.utils import raycast
from uplogic.utils import FLOATSAM
from uplogic.utils import SHIP
from uplogic.utils import WATER


class ULBuoy():

    def __init__(self) -> None:
        self._active = True

    def disable(self):
        self._active = False

    def enable(self):
        self._active = True

    def destroy(self):
        raise NotImplementedError


class ULFloatsam(ULBuoy):

    def __init__(self, game_object, buoyancy=1, height=200, align=True) -> None:
        super().__init__()
        self.game_object = game_object
        game_object[FLOATSAM] = self
        self.height = height
        self.buoyancy = buoyancy
        self.align = align
        logic.getCurrentScene().pre_draw.append(self.update)

    def update(self):
        if not self._active:
            return
        up = Vector((0, 0, 1))
        floatsam = self.game_object
        lindamp = .1
        wpos = floatsam.worldPosition
        obj, point, normal, direction = raycast(
            floatsam,
            wpos,
            up,
            self.height,
            WATER,
            True,
            True
        )
        if obj:
            lindamp = .8
            lift = (up * (wpos - point).length * self.buoyancy)
            floatsam.applyImpulse(
                wpos,
                vec_clamp(lift, max=self.buoyancy),
                False
            )
            if self.align:
                self.game_object.alignAxisToVect(normal, 2, .2)
        floatsam.linearDamping = lindamp
        floatsam.angularDamping = lindamp * .8

    def destroy(self):
        logic.getCurrentScene().pre_draw.remove(self.update)


class ULShip(ULBuoy):

    def __init__(self, game_object, buoyancy=1, height=200) -> None:
        super().__init__()
        self.game_object = game_object
        game_object[SHIP] = self
        print(game_object)
        self.height = height
        cs = sorted(game_object.childrenRecursive, key=lambda c: c.name)
        self.buoys = [c for c in cs if 'Buoy' in c.name]
        self.buoyancy = buoyancy
        logic.getCurrentScene().pre_draw.append(self.update)

    def update(self):
        if not self._active:
            return
        up = Vector((0, 0, 1))
        lifts = len(self.buoys)
        ship = self.game_object
        lindamp = .1
        for buoy in self.buoys:
            wpos = buoy.worldPosition
            obj, point, normal, direction = raycast(
                buoy,
                wpos,
                up,
                self.height,
                WATER,
                True,
                True,
                True
            )
            if obj:
                lindamp += (.7 / lifts)
                lift = (up * (wpos - point).length * self.buoyancy) / lifts
                ship.applyImpulse(
                    wpos,
                    vec_clamp(lift, max=self.buoyancy * 2 / lifts),
                    False
                )
        ship.linearDamping = lindamp
        ship.angularDamping = lindamp * .8

    def destroy(self):
        logic.getCurrentScene().pre_draw.remove(self.update)
