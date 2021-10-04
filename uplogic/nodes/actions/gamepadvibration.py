from bge import logic
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.nodes import not_met
from uplogic.nodes import is_waiting
from uplogic.nodes import debug


class ULGamepadVibration(ULActionNode):
    def __init__(self, axis=0):
        ULActionNode.__init__(self)
        self.condition = None
        self.index = None
        self.left = None
        self.right = None
        self.time = None
        self.done = None
        self.DONE = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self._set_ready()
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        index = self.get_socket_value(self.index)
        left = self.get_socket_value(self.left)
        right = self.get_socket_value(self.right)
        time = self.get_socket_value(self.time)
        if is_waiting(index, left, right, time):
            return

        if not logic.joysticks[index]:
            return
        joystick = logic.joysticks[index]
        if not joystick.hasVibration:
            debug('Joystick at index {} has no vibration!'.format(index))
            return

        joystick.strengthLeft = left
        joystick.strengthRight = right
        joystick.duration = int(round(time * 1000))

        joystick.startVibration()
        self.done = True
