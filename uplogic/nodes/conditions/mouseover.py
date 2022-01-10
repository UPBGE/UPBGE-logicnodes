from bge import logic
from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting


class ULMouseOver(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.game_object = None
        self._mouse_entered_status = False
        self._mouse_exited_status = False
        self._mouse_over_status = False
        self._point = None
        self._normal = None
        self.MOUSE_ENTERED = ULOutSocket(self, self._get_mouse_entered)
        self.MOUSE_EXITED = ULOutSocket(self, self._get_mouse_exited)
        self.MOUSE_OVER = ULOutSocket(self, self._get_mouse_over)
        self.POINT = ULOutSocket(self, self._get_point)
        self.NORMAL = ULOutSocket(self, self._get_normal)
        self._last_target = None

    def _get_mouse_entered(self):
        return self._mouse_entered_status

    def _get_mouse_exited(self):
        return self._mouse_exited_status

    def _get_mouse_over(self):
        return self._mouse_over_status

    def _get_point(self):
        return self._point

    def _get_normal(self):
        return self._normal

    def evaluate(self):
        game_object = self.get_input(self.game_object)
        if is_waiting(game_object):
            return
        self._set_ready()
        if is_invalid(game_object):
            self._mouse_entered_status = False
            self._mouse_exited_status = False
            self._mouse_over_status = False
            self._point = None
            self._normal = None
            return
        scene = game_object.scene
        camera = scene.active_camera
        distance = 2.0 * camera.getDistanceTo(game_object)
        mouse = logic.mouse
        mouse_position = mouse.position
        vec = 10.0 * camera.getScreenVect(*mouse_position)
        ray_target = camera.worldPosition - vec
        target, point, normal = self.network.ray_cast(
            camera,
            None,
            ray_target,
            None,
            False,
            distance
        )
        if not (target is self._last_target):  # mouse over a new object
            # was target, now it isn't -> exited
            if self._last_target is game_object:
                self._mouse_exited_status = True
                self._mouse_over_status = False
                self._mouse_entered_status = False
                self._point = None
                self._normal = None
            # wasn't target, now it is -> entered
            elif (target is game_object):
                self._mouse_entered_status = True
                self._mouse_over_status = False
                self._mouse_exited_status = False
                self._point = point
                self._normal = normal
            self._last_target = target
        else:  # the target has not changed
            # was target, still target -> over
            if self._last_target is game_object:
                self._mouse_entered_status = False
                self._mouse_exited_status = False
                self._mouse_over_status = True
                self._point = point
                self._normal = normal
            else:  # wans't target, still isn't target -> clear
                self._mouse_entered_status = False
                self._mouse_exited_status = False
                self._mouse_over_status = False
                self._point = None
                self._normal = None
