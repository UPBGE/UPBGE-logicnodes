from bge import logic
from bge.types import KX_GameObject as GameObject
from mathutils import Vector
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import debug
from uplogic.utils import not_met


class ULGamepadLook(ULActionNode):
    def __init__(self, axis=0):
        ULActionNode.__init__(self)
        self.axis: int = axis
        self.condition = None
        self.main_obj: GameObject = None
        self.head_obj: GameObject = None
        self.inverted: bool = None
        self.index: int = None
        self.sensitivity: float = None
        self.exponent: float = None
        self.use_cap_x: bool = None
        self.cap_x: Vector = None
        self.use_cap_y: bool = None
        self.cap_y: Vector = None
        self.threshold: float = None
        self.done: bool = None
        self.DONE = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        axis: int = self.get_input(self.axis)
        condition: GameObject = self.get_input(self.condition)
        if not_met(condition):
            return
        main_obj: GameObject = self.get_input(self.main_obj)
        head_obj: GameObject = self.get_input(self.head_obj)
        if is_invalid(head_obj):
            head_obj = main_obj
        if is_invalid(axis):
            debug('Gamepad Sticks Node: Invalid Controller Stick!')
            return
        inverted: bool = self.get_input(self.inverted)
        index: int = self.get_input(self.index)
        sensitivity: float = self.get_input(self.sensitivity)
        exponent: float = self.get_input(self.exponent)
        threshold: float = self.get_input(self.threshold)
        use_cap_x: Vector = self.get_input(self.use_cap_x)
        cap_x: Vector = self.get_input(self.cap_x)
        uppercapX: float = cap_x.x
        lowercapX: float = -cap_x.y
        use_cap_y: Vector = self.get_input(self.use_cap_y)
        cap_y: Vector = self.get_input(self.cap_y)
        uppercapY: float = cap_y.x
        lowercapY: float = -cap_y.y

        self._set_ready()
        if logic.joysticks[index]:
            joystick = logic.joysticks[index]
        else:
            debug('Gamepad Sticks Node: No Joystick at that Index!')
            return
        if is_invalid(joystick):
            return
        raw_values = joystick.axisValues
        if axis == 0:
            x, y = raw_values[0], raw_values[1]
        elif axis == 1:
            x, y = raw_values[2], raw_values[3]
        neg_x = -1 if x < 0 else 1
        neg_y = -1 if y < 0 else 1

        if -threshold < x < threshold:
            x = 0
        else:
            x = abs(x) ** exponent

        if -threshold < y < threshold:
            y = 0
        else:
            y = abs(y) ** exponent
        if x == y == 0:
            self.done = True
            return

        x *= neg_x
        y *= neg_y

        x = -x if inverted['x'] else x
        y = -y if inverted['y'] else y

        x *= sensitivity
        if use_cap_x:
            objectRotation = main_obj.localOrientation.to_euler()
            if objectRotation.z + x > uppercapX:
                x = 0
                objectRotation.z = uppercapX
                main_obj.localOrientation = objectRotation.to_matrix()

            if objectRotation.z + x < lowercapX:
                x = 0
                objectRotation.z = lowercapX
                main_obj.localOrientation = objectRotation.to_matrix()

        y *= sensitivity
        if use_cap_y:
            objectRotation = head_obj.localOrientation.to_euler()
            if objectRotation.y + y > uppercapY:
                y = 0
                objectRotation.y = uppercapY
                head_obj.localOrientation = objectRotation.to_matrix()

            if objectRotation.y + y < lowercapY:
                y = 0
                objectRotation.y = lowercapY
                head_obj.localOrientation = objectRotation.to_matrix()

        main_obj.applyRotation(Vector((0, 0, x)), True)
        head_obj.applyRotation(Vector((0, y, 0)), True)
        self.done = True
