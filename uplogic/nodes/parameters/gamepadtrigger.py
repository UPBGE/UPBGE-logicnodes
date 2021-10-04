from bge import logic
from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.nodes import is_invalid


class ULGamepadTrigger(ULParameterNode):
    def __init__(self, axis=0):
        ULParameterNode.__init__(self)
        self.axis = axis
        self.index = None
        self.sensitivity = None
        self.threshold = None
        self._value = None
        self.VAL = ULOutSocket(self, self.get_value)

    def get_x_axis(self):
        return self._value

    def evaluate(self):
        self._set_ready()
        axis = self.get_socket_value(self.axis)
        if is_invalid(axis):
            return
        index = self.get_socket_value(self.index)
        sensitivity = self.get_socket_value(self.sensitivity)
        threshold = self.get_socket_value(self.threshold)
        if logic.joysticks[index]:
            joystick = logic.joysticks[index]
        else:
            self._x_axis_values = 0
            self._y_axis_values = 0
            return
        if is_invalid(joystick):
            return
        value = joystick.axisValues[4] if axis == 0 else joystick.axisValues[5]

        if -threshold < value < threshold:
            value = 0
        self._value = value * sensitivity
