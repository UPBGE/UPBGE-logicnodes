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
        socket = self.get_output('pressed')
        if socket is None:
            mouse_button = self.get_input(self.mouse_button_code)
            if is_waiting(mouse_button):
                return STATUS_WAITING
            self._set_ready()
            mstat = self.network.mouse_events[mouse_button]
            if self.pulse:
                return self.set_output(
                    'pressed',
                    (
                        mstat.active or
                        mstat.activated
                    )
                )
            else:
                return self.set_output(
                    'pressed',
                    (mstat.activated)
                )
        return socket

    def evaluate(self):
        self._set_ready()
