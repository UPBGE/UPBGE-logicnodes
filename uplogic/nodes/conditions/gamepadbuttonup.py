from bge import logic
from uplogic.nodes import GEConditionNode
from uplogic.nodes import GEOutSocket
from uplogic.nodes import STATUS_WAITING
from uplogic.nodes import is_invalid


class GEGamepadButtonUp(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.pulse = False
        self.button = 0
        self.index = None
        self._last_value = False
        self._up_value = None
        self.BUTTON = GEOutSocket(self, self.get_button)
        self.initialized = False

    def get_button(self):
        pressed = False
        index = self.get_socket_value(self.index)
        if logic.joysticks[index]:
            joystick = logic.joysticks[index]
        else:
            return STATUS_WAITING
        if is_invalid(joystick):
            return STATUS_WAITING

        button_down = True if self.button in joystick.activeButtons else False

        if button_down != self._last_value and not button_down:
            if not self.pulse and not self.initialized:
                self.initialized = True
            pressed = True
        elif (pressed and self.initialized) or button_down:

            pressed = False
            self.initialized = False
        elif not (self.initialized and button_down) and pressed:
            pressed = True

        self._last_value = button_down
        return pressed

    def evaluate(self):
        self._set_ready()
