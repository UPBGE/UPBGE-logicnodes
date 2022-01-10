from bge import logic
from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULGamepadTrigger(ULParameterNode):
    def __init__(self, axis=0):
        ULParameterNode.__init__(self)
        self.axis = axis
        self.index = None
        self.sensitivity = None
        self.threshold = None
        self._value = None
        self.VAL = ULOutSocket(self, self.get_value)

    def get_value(self):
        socket = self.get_output('changed')
        if socket is None:
            axis = self.get_input(self.axis)
            if is_invalid(axis):
                return STATUS_WAITING
            index = self.get_input(self.index)
            sensitivity = self.get_input(self.sensitivity)
            threshold = self.get_input(self.threshold)
            if logic.joysticks[index]:
                joystick = logic.joysticks[index]
            else:
                self._x_axis_values = 0
                self._y_axis_values = 0
                return STATUS_WAITING
            if is_invalid(joystick):
                return STATUS_WAITING
            value = (
                joystick.axisValues[4] if axis == 0
                else joystick.axisValues[5]
            )

            if -threshold < value < threshold:
                value = 0
            return self.set_output('trigger', value * sensitivity)
        return socket

    def evaluate(self):
        self._set_ready()
