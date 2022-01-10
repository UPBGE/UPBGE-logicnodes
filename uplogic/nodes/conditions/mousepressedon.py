from bge import logic
from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting


class ULMousePressedOn(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.game_object = None
        self.mouse_button = None
        self.OUT = ULOutSocket(self, self.get_changed)

    def get_changed(self):
        socket = self.get_output('changed')
        if socket is None:
            mouse_button = self.get_input(self.mouse_button)
            game_object = self.get_input(self.game_object)
            if is_waiting(mouse_button, game_object):
                return STATUS_WAITING
            if mouse_button is None:
                return STATUS_WAITING
            if is_invalid(game_object):
                return STATUS_WAITING
            mstat = self.network.mouse_events[mouse_button]
            if not mstat.activated:
                return (False)
            mpos = logic.mouse.position
            camera = logic.getCurrentScene().active_camera
            vec = 10 * camera.getScreenVect(*mpos)
            ray_target = camera.worldPosition - vec
            distance = camera.getDistanceTo(game_object) * 2.0
            t, p, n = self.network.ray_cast(
                camera,
                None,
                ray_target,
                None,
                False,
                distance
            )
            return self.set_output(
                'changed',
                (t == game_object)
            )
        return socket

    def evaluate(self):
        self._set_ready()
