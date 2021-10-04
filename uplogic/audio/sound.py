
from bge import logic
from uplogic.utils import compute_distance
from mathutils import Vector
import aud


class ULSound3D():
    sounds = []
    speaker = None
    occlusion = False
    _clear_sound = 1
    _sustained = 1

    def __init__(
        self,
        file=None,
        aud_system=None,
        occlusion=False,
        speaker=None,
        transition=.1,
        cutoff=.1,
        volume=1,
        pitch=1,
        attenuation=1,
        distance_ref=1,
        cone_angle=[360, 360],
        cone_outer_volume=0,
        loop_count=1
    ):
        if not (file and aud_system and speaker):
            return
        self.aud_system = aud_system
        self.speaker = speaker
        self.occlusion = occlusion
        self.volume = volume
        self.pitch = pitch
        self.cone_outer_volume = cone_outer_volume
        self.transition = transition
        soundfile = logic.expandPath(file)
        sound = aud.Sound(soundfile)
        device = aud_system.device
        handle = device.play(sound)
        if occlusion:
            soundlow = aud.Sound.lowpass(sound, 4000*cutoff, .5)
            handlelow = device.play(soundlow)
            self.handles = [speaker, [handle, handlelow]]
        else:
            self.handles = [speaker, [handle]]
        for handle in self.handles[1]:
            handle.relative = False
            handle.location = speaker.worldPosition
            if speaker.mass:
                handle.velocity = getattr(
                    speaker,
                    'worldLinearVelocity',
                    Vector((0, 0, 0))
                )
            handle.attenuation = attenuation
            handle.orientation = speaker.worldOrientation.to_quaternion()
            handle.pitch = pitch
            handle.volume = volume
            handle.distance_reference = distance_ref
            handle.distance_maximum = 1000
            handle.cone_angle_inner = cone_angle[0]
            handle.cone_angle_outer = cone_angle[1]
            handle.cone_volume_outer = cone_outer_volume * volume
        self.aud_system.add(self)

    def update(self):
        speaker = self.speaker
        if not speaker:
            self.aud_system.remove(self)
        for i, handle in enumerate(self.handles[1]):
            if not handle.status:
                self.aud_system.remove(self)
                return
            handle.pitch = self.pitch
            handle.location = speaker.worldPosition
            handle.orientation = (
                speaker
                .worldOrientation
                .to_quaternion()
            )
            if speaker.mass:
                handle.velocity = getattr(
                    speaker,
                    'worldLinearVelocity',
                    Vector((0, 0, 0))
                )
            if self.occlusion:
                transition = self.transition
                cam = logic.getCurrentScene().active_camera
                occluder, point, normal = cam.rayCast(
                    speaker.worldPosition,
                    cam.worldPosition,
                    compute_distance(speaker, cam),
                    xray=False
                )
                occluded = False
                penetration = 1
                while occluder:
                    if occluder is speaker:
                        break
                    sound_occluder = occluder.blenderObject.get(
                        'sound_occluder',
                        True
                    )
                    if sound_occluder:
                        occluded = True
                        block = occluder.blenderObject.get(
                            'sound_blocking',
                            .1
                        )
                        if penetration > 0:
                            penetration -= block
                        else:
                            penetration = 0
                    occluder, point, normal = occluder.rayCast(
                        speaker.worldPosition,
                        point,
                        compute_distance(speaker, point),
                        xray=False
                    )
                cs = self._clear_sound
                if occluded and cs > 0:
                    self._clear_sound -= transition
                elif not occluded and cs < 1:
                    self._clear_sound += transition
                if self._clear_sound < 0:
                    self._clear_sound = 0
                sustained = self._sustained
                if sustained > penetration:
                    self._sustained -= transition / 10
                elif sustained < penetration:
                    self._sustained += transition / 10
                mult = (
                    cs * sustained
                    if not i
                    else (1 - cs) * sustained
                )
                handle.volume = self.volume * mult
                handle.cone_volume_outer = (
                    self.cone_outer_volume *
                    self.volume *
                    mult
                )
