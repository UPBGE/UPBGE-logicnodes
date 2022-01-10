from mathutils import Vector
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULCameraRayCast(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.camera = None
        self.aim = None
        self.property_name = None
        self.xray = None
        self.distance = None
        self._picked_object = None
        self._picked_point = None
        self._picked_normal = None
        self.PICKED_OBJECT = ULOutSocket(self, self.get_picked_object)
        self.PICKED_POINT = ULOutSocket(self, self.get_picked_point)
        self.PICKED_NORMAL = ULOutSocket(self, self.get_picked_normal)

    def get_picked_object(self):
        return self._picked_object

    def get_picked_point(self):
        return self._picked_point

    def get_picked_normal(self):
        return self._picked_normal

    def evaluate(self):
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        camera = self.get_input(self.camera)
        aim = self.get_input(self.aim)
        property_name = self.get_input(self.property_name)
        xray = self.get_input(self.xray)
        distance = self.get_input(self.distance)
        if is_waiting(camera, aim, property_name, xray, distance):
            return
        self._set_ready()
        if not condition:
            self._set_value(False)
            self._out_normal = None
            self._out_object = None
            self._out_point = None
            return
        if is_invalid(camera):
            return
        if is_invalid(aim):
            return
        obj, point, normal = None, None, None
        # assume screen coordinates
        if isinstance(aim, Vector) and len(aim) == 2:
            vec = 10 * camera.getScreenVect(aim[0], aim[1])
            ray_target = camera.worldPosition - vec
            aim = ray_target
        if not property_name:
            obj, point, normal = camera.rayCast(aim, None, distance)
        else:
            obj, point, normal = camera.rayCast(
                aim,
                None,
                distance,
                property_name,
                xray=xray
            )
        self._set_value(obj is not None)
        self._picked_object = obj
        self._picked_point = point
        self._picked_normal = normal
