from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.nodes import STATUS_WAITING
from uplogic.nodes import is_waiting


class ULMouseReleased(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.pulse = False
        self.mouse_button_code = None
        self.network = None
        self.OUT = ULOutSocket(self, self.get_changed)

    def get_changed(self):
        mouse_button = self.get_socket_value(self.mouse_button_code)
        if is_waiting(mouse_button):
            return STATUS_WAITING
        mstat = self.network.mouse_events[mouse_button]
        if self.pulse:
            return (
                mstat.released or
                mstat.inactive
            )
        else:
            return (mstat.released)

    def setup(self, network):
        self.network = network

    def evaluate(self):
        self._set_ready()
