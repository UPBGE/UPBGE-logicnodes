from bge import logic
from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULGamepadButton(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.pulse = False
        self.button = 0
        self.index = None
        self._button = None
        self.BUTTON = ULOutSocket(self, self.get_button)
        self.initialized = False

    def get_button(self):
        index = self.get_socket_value(self.index)
        if logic.joysticks[index]:
            joystick = logic.joysticks[index]
        else:
            self._button = False
            self._set_ready()
            return STATUS_WAITING
        if is_invalid(joystick):
            return STATUS_WAITING
        if self.button in joystick.activeButtons:
            if not self.initialized:
                pressed = True
            else:
                pressed = False
            if not self.pulse:
                self.initialized = True
        else:
            pressed = False
            self.initialized = False
        return pressed

    def evaluate(self):
        self._set_ready()
