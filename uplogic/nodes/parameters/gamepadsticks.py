from bge import logic
from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid


class ULGamepadSticks(ULParameterNode):
    def __init__(self, axis=0):
        ULParameterNode.__init__(self)
        self.axis = axis
        self.inverted = None
        self.index = None
        self.sensitivity = None
        self.threshold = None
        self._x_axis_values = None
        self._y_axis_values = None
        self.X = ULOutSocket(self, self.get_x_axis)
        self.Y = ULOutSocket(self, self.get_y_axis)

    def get_x_axis(self):
        x = self.raw_values[0]
        if -self.threshold < x < self.threshold:
            x = 0
        return x * self.sensitivity

    def get_y_axis(self):
        y = self.raw_values[1]
        if -self.threshold < y < self.threshold:
            y = 0
        return y * self.sensitivity

    def evaluate(self):
        self._set_ready()
        index = self.get_socket_value(self.index)

        if logic.joysticks[index]:
            joystick = logic.joysticks[index]
        else:
            self._x_axis_values = 0
            self._y_axis_values = 0
            return
        if is_invalid(joystick):
            return
        axis = self.get_socket_value(self.axis)
        raw_values = joystick.axisValues
        if axis == 0:
            self.raw_values = [raw_values[0], raw_values[1]]
        elif axis == 1:
            self.raw_values = [raw_values[2], raw_values[3]]
        inverted = self.get_socket_value(self.inverted)
        sensitivity = self.get_socket_value(self.sensitivity)
        self.sensitivity = -sensitivity if inverted else sensitivity
        self.threshold = self.get_socket_value(self.threshold)
