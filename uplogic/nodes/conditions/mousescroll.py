from uplogic.nodes import GEConditionNode
from uplogic.nodes import is_waiting


class GEMouseScrolled(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.wheel_direction = None

    def evaluate(self):
        wd = self.get_socket_value(self.wheel_direction)
        if is_waiting(wd):
            return
        self._set_ready()
        if wd is None:
            return
        elif wd == 1:  # UP
            self._set_value(self.network.mouse_wheel_delta == 1)
        elif wd == 2:  # DOWN
            self._set_value(self.network.mouse_wheel_delta == -1)
        elif wd == 3:  # UP OR DOWN
            self._set_value(self.network.mouse_wheel_delta != 0)
