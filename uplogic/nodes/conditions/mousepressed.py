from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting


class ULMousePressed(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.pulse = False
        self.mouse_button_code = None
        self.OUT = ULOutSocket(self, self.get_pressed)

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
