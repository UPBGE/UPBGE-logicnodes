from uplogic.nodes import GEConditionNode
from uplogic.nodes import GEOutSocket
from uplogic.nodes import STATUS_WAITING
from uplogic.nodes import is_waiting


class GEMousePressed(GEConditionNode):
    def __init__(self):
        super()
        self.pulse = False
        self.mouse_button_code = None
        self.OUT = GEOutSocket(self, self.get_pressed)

    def get_pressed(self):
        mouse_button = self.get_socket_value(self.mouse_button_code)
        if is_waiting(mouse_button):
            return STATUS_WAITING
        self._set_ready()
        mstat = self.network.mouse_events[mouse_button]
        if self.pulse:
            return (
                mstat.active or
                mstat.activated
            )
        else:
            return (mstat.activated)

    def evaluate(self):
        self._set_ready()
