from bge import logic
from uplogic.audio import ULSound3D
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULStartSound3D(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.sound = None
        self.occlusion = None
        self.transition = None
        self.cutoff = None
        self.speaker = None
        self.device = None
        self.loop_count = None
        self.pitch = None
        self.volume = None
        self.attenuation = None
        self.distance_ref = None
        self.cone_angle = None
        self.cone_outer_volume = None
        self.done = None
        self.on_finish = False
        self._clear_sound = 1
        self._sustained = 1
        self._handle = None
        self.DONE = ULOutSocket(self, self.get_done)
        self.ON_FINISH = ULOutSocket(self, self.get_on_finish)
        self.HANDLE = ULOutSocket(self, self.get_handle)

    def get_handle(self):
        return self._handle

    def get_on_finish(self):
        if not self._handle:
            return False
        if self._handle.finished:
            self._handle = None
            return True
        return False

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        self.on_finish = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        speaker = self.get_socket_value(self.speaker)
        transition = self.get_socket_value(self.transition)
        occlusion = self.get_socket_value(self.occlusion)
        volume = self.get_socket_value(self.volume)
        cone_outer_volume = self.get_socket_value(self.cone_outer_volume)
        attenuation = self.get_socket_value(self.attenuation)
        cutoff = self.get_socket_value(self.cutoff)
        file = self.get_socket_value(self.sound)
        loop_count = self.get_socket_value(self.loop_count)
        distance_ref = self.get_socket_value(self.distance_ref)
        cone_angle = self.get_socket_value(self.cone_angle)
        pitch = self.get_socket_value(self.pitch) * logic.getTimeScale()
        self._set_ready()

        if is_invalid(file):
            return
        self._handle = ULSound3D(
            speaker,
            file,
            'default',
            occlusion,
            transition,
            cutoff,
            volume,
            pitch,
            attenuation,
            distance_ref,
            [cone_angle.x, cone_angle.y],
            cone_outer_volume,
            loop_count
        )
        self.done = True
