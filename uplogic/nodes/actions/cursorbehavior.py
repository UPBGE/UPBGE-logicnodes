from bge import logic
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULCursorBehavior(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.cursor_object = None
        self.world_z = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        self._set_ready()
        cursor_object = self.get_input(self.cursor_object)
        if is_invalid(cursor_object):
            return
        condition = self.get_input(self.condition)
        if not_met(condition):
            if cursor_object.visible:
                cursor_object.setVisible(False, True)
            return
        camera = logic.getCurrentScene().active_camera
        world_z = self.get_input(self.world_z)
        if not cursor_object.visible:
            cursor_object.setVisible(True, True)
        else:
            x = self.network._last_mouse_position[0]
            y = self.network._last_mouse_position[1]
            direction = camera.getScreenVect(x, y)
            origin = camera.worldPosition
            aim = direction * -world_z
            point = origin + aim
            cursor_object.worldOrientation = camera.worldOrientation
            cursor_object.worldPosition = point
        self.done = True
