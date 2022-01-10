from bge import render
from bge import logic
from mathutils import Vector
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import not_met
from uplogic.utils import interpolate


class ULMouseLook(ULActionNode):
    x = None
    y = None
    screen_center = None
    center = None
    mouse = None

    def __init__(self):
        ULActionNode.__init__(self)
        self.axis = None
        self.condition = None
        self.game_object_x = None
        self.game_object_y = None
        self.inverted = None
        self.sensitivity = None
        self.use_cap_z = None
        self.cap_z = None
        self.use_cap_z = None
        self.cap_y = None
        self.smooth = None
        self.initialized = False
        self._x = 0
        self._y = 0
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.use_local_head = False
        self.get_data()
        self.mouse.position = self.screen_center

    def get_done(self):
        return self.done

    def get_x_obj(self):
        game_object_x = self.get_input(self.game_object_x)
        return game_object_x

    def get_y_obj(self):
        game_object_y = self.get_input(self.game_object_y)
        if is_invalid(game_object_y):
            game_object_y = self.get_x_obj()
        elif game_object_y is not self.get_x_obj():
            self.use_local_head = True
        return game_object_y

    def get_data(self):
        self.x = render.getWindowWidth()//2
        self.y = render.getWindowHeight()//2
        self.screen_center = (
            self.x / render.getWindowWidth(),
            self.y / render.getWindowHeight()
        )
        self.center = Vector(self.screen_center)
        self.mouse = logic.mouse

    def evaluate(self):
        self.done = False
        self.get_data()
        condition = self.get_input(self.condition)
        if not_met(condition):
            self.initialized = False
        elif not self.initialized:
            self.mouse.position = self.screen_center
            self.initialized = True
            return
        game_object_x = self.get_x_obj()
        game_object_y = self.get_y_obj()
        sensitivity = self.get_input(self.sensitivity) * 1000
        use_cap_z = self.get_input(self.use_cap_z)
        use_cap_y = self.get_input(self.use_cap_y)
        cap_z = self.get_input(self.cap_z)
        lowercapX = cap_z.y
        uppercapX = cap_z.x
        cap_y = self.get_input(self.cap_y)
        lowercapY = cap_y.x
        uppercapY = cap_y.y
        inverted = self.get_input(self.inverted)
        smooth = 1 - (self.get_input(self.smooth) * .99)
        self._set_ready()

        if is_invalid(game_object_x):
            return

        if condition:
            mouse_position = Vector(self.mouse.position)
            offset = (mouse_position - self.center) * -0.002
        else:
            offset = Vector((0, 0))

        if inverted.get('y', False) is False:
            offset.y = -offset.y
        if inverted.get('x', False) is True:
            offset.x = -offset.x
        offset *= sensitivity

        self._x = offset.x = interpolate(self._x, offset.x, smooth)
        self._y = offset.y = interpolate(self._y, offset.y, smooth)

        if use_cap_z:
            objectRotation = game_object_x.localOrientation.to_euler()

            if objectRotation.z + offset.x > uppercapX:
                offset.x = 0
                objectRotation.z = uppercapX
                game_object_x.localOrientation = objectRotation.to_matrix()

            if objectRotation.z + offset.x < lowercapX:
                offset.x = 0
                objectRotation.z = lowercapX
                game_object_x.localOrientation = objectRotation.to_matrix()

        game_object_x.applyRotation((0, 0, offset.x), self.use_local_head)

        rot_axis = 1 - self.axis
        if use_cap_y:
            objectRotation = game_object_y.localOrientation.to_euler()

            if objectRotation[rot_axis] + offset.y > uppercapY:
                objectRotation[rot_axis] = uppercapY
                game_object_y.localOrientation = objectRotation.to_matrix()
                offset.y = 0

            if objectRotation[rot_axis] + offset.y < lowercapY:
                objectRotation[rot_axis] = lowercapY
                game_object_y.localOrientation = objectRotation.to_matrix()
                offset.y = 0

        rot = [0, 0, 0]
        rot[1-self.axis] = offset.y
        game_object_y.applyRotation((*rot, ), True)
        if self.mouse.position != self.screen_center and condition:
            self.mouse.position = self.screen_center
        self.done = True
