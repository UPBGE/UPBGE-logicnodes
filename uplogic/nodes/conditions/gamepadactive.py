from bge import logic
from uplogic.nodes import ULConditionNode


class ULGamepadActive(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.index = None

    def evaluate(self):
        index = self.get_socket_value(self.index)
        if logic.joysticks[index]:
            joystick = logic.joysticks[index]
        else:
            self._button = False
            self._set_ready()
            return
        self._set_ready()
        axis_active = False
        for x in joystick.axisValues:
            if x < -.1 or x > .1:
                axis_active = True
                break
        self._set_value(
            joystick.activeButtons or
            axis_active
        )
