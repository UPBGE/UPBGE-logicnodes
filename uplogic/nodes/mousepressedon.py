from bge import logic
from uplogic.nodes import GEConditionNode
from uplogic.nodes import GEOutSocket
from uplogic.nodes import STATUS_WAITING
from uplogic.nodes import is_invalid
from uplogic.nodes import is_waiting


class GEMousePressedOn(GEConditionNode):
    def __init__(self):
        super()
        self.game_object = None
        self.mouse_button = None
        self.OUT = GEOutSocket(self, self.get_changed)

    def get_changed(self):
        mouse_button = self.get_socket_value(self.mouse_button)
        game_object = self.get_socket_value(self.game_object)
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
        return (t == game_object)

    def evaluate(self):
        self._set_ready()
