from bge import logic
from uplogic.audio import ULSound3D
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULStartSpeaker(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.occlusion = None
        self.transition = None
        self.cutoff = None
        self.speaker = None
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
        condition = self.get_input(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        speaker = self.get_input(self.speaker)
        transition = self.get_input(self.transition)
        occlusion = self.get_input(self.occlusion)
        cutoff = self.get_input(self.cutoff)
        loop_count = self.get_input(self.loop_count)
        bl_speaker = speaker.blenderObject.data
        file = bl_speaker.sound.filepath
        if not file:
            return
        volume = bl_speaker.volume
        pitch = bl_speaker.pitch * logic.getTimeScale()
        attenuation = bl_speaker.attenuation
        distance_ref = bl_speaker.distance_reference
        cone_inner = bl_speaker.cone_angle_inner
        cone_outer = bl_speaker.cone_angle_outer
        cone_outer_volume = bl_speaker.cone_volume_outer
        self._set_ready()

        if is_invalid(file):
            return
        self._handle = ULSound3D(
            file,
            speaker,
            'ln_audio_system',
            occlusion,
            transition,
            cutoff,
            volume,
            pitch,
            attenuation,
            distance_ref,
            [cone_inner, cone_outer],
            cone_outer_volume,
            loop_count
        )
        self.done = True
