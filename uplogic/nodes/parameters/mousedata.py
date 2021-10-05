from mathutils import Vector
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_READY


class ULMouseData(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.MX = ULOutSocket(self, self.getmx)
        self.MY = ULOutSocket(self, self.getmy)
        self.MDX = ULOutSocket(self, self.getmdx)
        self.MDY = ULOutSocket(self, self.getmdy)
        self.MDWHEEL = ULOutSocket(self, self.getmdwheel)
        self.MXY0 = ULOutSocket(self, self.getmxyz)
        self.MDXY0 = ULOutSocket(self, self.getmdxyz)

    def getmx(self):
        return self.network._last_mouse_position[0]

    def getmy(self):
        return self.network._last_mouse_position[1]

    def getmdx(self):
        return self.network.mouse_motion_delta[0]

    def getmdy(self):
        return self.network.mouse_motion_delta[1]

    def getmdwheel(self):
        return self.network.mouse_wheel_delta

    def getmxyz(self):
        mp = self.network._last_mouse_position
        return Vector((mp[0], mp[1], 0))

    def getmdxyz(self):
        mp = self.network.mouse_motion_delta
        return Vector((mp[0], mp[1], 0))

    def evaluate(self):
        self._set_ready()

    def has_status(self, status):
        return status is STATUS_READY
