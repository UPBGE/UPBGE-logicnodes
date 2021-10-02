from mathutils import Vector
from uplogic.nodes import GEOutSocket
from uplogic.nodes import GEParameterNode
from uplogic.nodes import STATUS_READY


class GEMouseData(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.MX = GEOutSocket(self, self.getmx)
        self.MY = GEOutSocket(self, self.getmy)
        self.MDX = GEOutSocket(self, self.getmdx)
        self.MDY = GEOutSocket(self, self.getmdy)
        self.MDWHEEL = GEOutSocket(self, self.getmdwheel)
        self.MXY0 = GEOutSocket(self, self.getmxyz)
        self.MDXY0 = GEOutSocket(self, self.getmdxyz)

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
