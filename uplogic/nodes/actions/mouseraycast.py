from bge import logic
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULMouseRayCast(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.distance = None
        self.property = None
        self.xray = None
        self.camera = None
        self._set_value(False)
        self._out_object = None
        self._out_normal = None
        self._out_point = None
        self.OUTOBJECT = ULOutSocket(self, self.get_out_object)
        self.OUTNORMAL = ULOutSocket(self, self.get_out_normal)
        self.OUTPOINT = ULOutSocket(self, self.get_out_point)

    def get_out_object(self):
        return self._out_object

    def get_out_normal(self):
        return self._out_normal

    def get_out_point(self):
        return self._out_point

    def evaluate(self):
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        distance = self.get_input(self.distance)
        property_name = self.get_input(self.property)
        xray = self.get_input(self.xray)
        camera = self.get_input(self.camera)
        if is_waiting(distance, property_name, xray, camera):
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
        mpos = logic.mouse.position
        vec = 10 * camera.getScreenVect(*mpos)
        ray_target = camera.worldPosition - vec
        target, point, normal = self.network.ray_cast(
            camera,
            None,
            ray_target,
            property_name,
            xray,
            distance
        )
        self._set_value(target is not None)
        self._out_object = target
        self._out_normal = normal
        self._out_point = point
