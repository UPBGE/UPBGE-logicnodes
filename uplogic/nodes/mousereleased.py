from uplogic.nodes import GEConditionNode
from uplogic.nodes import GEOutSocket
from uplogic.nodes import STATUS_WAITING
from uplogic.nodes import is_waiting


class GEMouseReleased(GEConditionNode):
    def __init__(self):
        super()
        self.pulse = False
        self.mouse_button_code = None
        self.network = None
        self.OUT = GEOutSocket(self, self.get_changed)

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
