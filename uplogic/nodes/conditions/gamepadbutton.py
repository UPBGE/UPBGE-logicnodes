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
        socket = self.get_output('button')
        if socket is None:
            index = self.get_input(self.index)
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
            return self.set_output(
                'button',
                pressed
            )
        return socket

    def evaluate(self):
        self._set_ready()
