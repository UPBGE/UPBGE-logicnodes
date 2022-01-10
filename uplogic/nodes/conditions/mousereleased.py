from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting


class ULMouseReleased(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.pulse = False
        self.mouse_button_code = None
        self.network = None
        self.OUT = ULOutSocket(self, self.get_changed)

    def get_changed(self):
        socket = self.get_output('changed')
        if socket is None:
            mouse_button = self.get_input(self.mouse_button_code)
            if is_waiting(mouse_button):
                return STATUS_WAITING
            mstat = self.network.mouse_events[mouse_button]
            if self.pulse:
                return self.set_output(
                    'changed',
                    (
                        mstat.released or
                        mstat.inactive
                    )
                )
            else:
                return self.set_output(
                    'changed',
                    (mstat.released)
                )
        return socket

    def setup(self, network):
        self.network = network

    def evaluate(self):
        self._set_ready()
