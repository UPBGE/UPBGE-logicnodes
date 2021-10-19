from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING, is_invalid


class ULWorldPosition(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.camera = None
        self.screen_x = None
        self.screen_y = None
        self.world_z = None
        self.OUT = ULOutSocket(self, self.get_pos)

    def get_pos(self):
        camera = self.get_socket_value(self.camera)
        screen_x = self.get_socket_value(self.screen_x)
        screen_y = self.get_socket_value(self.screen_y)
        world_z = self.get_socket_value(self.world_z)
        if (
            is_invalid(camera) or
            (screen_x is None) or
            (screen_y is None) or
            (world_z is None)
        ):
            return STATUS_WAITING
        else:
            direction = camera.getScreenVect(screen_x, screen_y)
            origin = camera.worldPosition
            aim = direction * -world_z
            point = origin + (aim)
            return point

    def evaluate(self):
        self._set_ready()
