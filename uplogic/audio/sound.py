'''TODO: Documentation
'''

from bge import logic
from bge.types import KX_GameObject as GameObject
from bpy.types import AnyType
from mathutils import Vector
from uplogic.audio import ULAudioSystem
from uplogic.data import GlobalDB
from uplogic.events import schedule_callback
from uplogic.utils import interpolate
import aud


class ULReverb():

    volume: float

    def __init__(
        self,
        parent,
        sound,
        handle
    ):
        self.volume = 0
        self.parent = parent
        self.handle = handle
        self.aud_system = parent.aud_system
        self.samples = []
        schedule_callback(self.add_sample, 1/60, sound)

    def add_sample(self, sound):
        handle = self.handle
        sample = self.aud_system.device.play(sound)
        self.samples.append(sample)
        sample.loop_count = handle.loop_count
        sample.position = handle.position - (.0001 * len(self.samples))
        sample.relative = handle.relative
        sample.location = handle.location
        sample.velocity = handle.velocity
        sample.attenuation = handle.attenuation
        sample.orientation = handle.orientation
        sample.pitch = handle.pitch
        sample.volume = 0
        sample.distance_reference = handle.distance_reference
        sample.distance_maximum = handle.distance_maximum
        sample.cone_angle_inner = handle.cone_angle_inner
        sample.cone_angle_outer = handle.cone_angle_outer
        sample.cone_volume_outer = handle.cone_volume_outer
        if len(self.samples) < 30:
            schedule_callback(self.add_sample, 1/60, sound)

    def update(self):
        sample_count = self.aud_system.bounces
        use_reverb = (
            self.aud_system.reverb
        )
        handle = self.handle
        if not use_reverb or sample_count == 0:
            if self.volume < .001:
                return
            else:
                self.volume = interpolate(self.volume, 0, .1)
        else:
            parent = self.parent
            target_vol = (
                parent.volume / 10 if
                parent.occluded else
                parent.volume / 2
            )
            self.volume = interpolate(self.volume, target_vol, .1)
        for idx, sample in enumerate(self.samples):
            if not sample.status:
                sample.stop()
                continue
            if idx > sample_count:
                sample.volume = 0
                continue
            mult = idx/sample_count
            loc = handle.location
            lloc = self.aud_system.device.listener_location
            loc = (loc[0]-lloc[0], loc[1]-lloc[1], loc[2]-lloc[2])
            sample.location = (
                -(loc[0]-lloc[0]),
                -(loc[1]-lloc[1]),
                -(loc[2]-lloc[2])
            )
            sample.velocity = handle.velocity
            sample.attenuation = handle.attenuation
            sample.orientation = handle.orientation
            sample.distance_maximum = handle.distance_maximum
            sample.cone_angle_inner = handle.cone_angle_inner
            sample.pitch = handle.pitch
            sample.volume = (1-(handle.volume * (mult**2)))*.5 * self.volume
            sample.cone_volume_outer = handle.cone_volume_outer


class ULSound():
    '''TODO: Documentation
    '''

    sound = None
    finished: bool
    pitch: float
    volume: float
    aud_system: ULAudioSystem

    def stop(self):
        '''TODO: Documentation
        '''
        self.sound.stop()

    def get_aud_sys(self, name: str):
        '''TODO: Documentation
        '''
        aud_systems = GlobalDB.retrieve('uplogic.audio')
        if aud_systems.check(name):
            return aud_systems.get(name)
        else:
            return ULAudioSystem(name)


class ULSound2D(ULSound):
    '''TODO: Documentation
    '''
    sound: aud.Sound

    def __init__(
        self,
        file: str = '',
        aud_system: str = 'default',
        volume: float = 1,
        pitch: float = 1,
        loop_count: int = 1
    ):
        if not (file and aud_system):
            return
        self.pitch = pitch
        self.volume = volume
        self.aud_system = self.get_aud_sys(aud_system)
        soundfile = logic.expandPath(file)
        sound = aud.Sound(soundfile)
        device = self.aud_system.device
        handle = self.sound = device.play(sound)
        handle.relative = True
        handle.pitch = pitch
        handle.volume = volume
        handle.loop_count = loop_count
        self.aud_system.add(self)

    def update(self):
        '''TODO: Documentation
        '''
        handle = self.sound
        if not handle.status:
            self.finished = True
            self.aud_system.remove(self)
            return
        handle.pitch = self.pitch * logic.getTimeScale()
        handle.volume = self.volume


class ULSound3D(ULSound):
    '''TODO: Documentation
    '''
    sounds: list
    speaker: GameObject
    occlusion: bool
    location: Vector
    cone_outer_volume: float
    transition: float
    soundpath: str
    reverb: bool
    bounces: int
    _clear_sound: float
    _sustained: float
    reverb_samples: ULReverb

    def __init__(
        self,
        speaker: GameObject = None,
        file: str = '',
        aud_system: str = 'default',
        occlusion: bool = False,
        transition_speed: float = .1,
        cutoff_frequency: float = .1,
        volume: float = 1,
        pitch: float = 1,
        attenuation: float = 1,
        distance_ref: float = 1,
        cone_angle: list[float] = [360, 360],
        cone_outer_volume: float = 0,
        loop_count: int = -1,
        reverb=False
    ):
        if not (file and aud_system and speaker):
            return
        self._clear_sound = 1
        self._sustained = 1
        self.occluded = False
        self.sounds = []
        self.reverb_samples = None
        self.aud_system = self.get_aud_sys(aud_system)
        self.speaker = speaker
        self.reverb = reverb
        self.occlusion = occlusion
        self.volume = volume
        self.pitch = pitch
        self.cone_outer_volume = cone_outer_volume
        self.transition = transition_speed
        soundfile = logic.expandPath(file)
        sound = self.soundpath = aud.Sound(soundfile)
        device = self.aud_system.device
        handle = device.play(sound)
        if occlusion:
            soundlow = aud.Sound.lowpass(sound, 4400 * cutoff_frequency, .5)
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
            handle.loop_count = loop_count
            handle.cone_volume_outer = cone_outer_volume * volume
        if self.aud_system.reverb and self.reverb:
            self.reverb_samples = ULReverb(
                self,
                sound,
                self.handles[1][0]
            )
        self.aud_system.add(self)

    def update(self):
        '''TODO: Documentation
        '''
        aud_system = self.aud_system
        speaker = self.speaker
        location = speaker.worldPosition
        if not speaker:
            self.finished = True
            aud_system.remove(self)
            return
        for i, handle in enumerate(self.handles[1]):
            if not handle.status:
                self.finished = True
                aud_system.remove(self)
                return
            handle.pitch = self.pitch * logic.getTimeScale()
            handle.location = location
            handle.orientation = (
                speaker
                .worldOrientation
                .to_quaternion()
            )
            getattr(speaker, 'worldLinearVelocity', Vector((0, 0, 0)))
            if self.occlusion:
                transition = self.transition
                cam = self.aud_system.listener
                occluder, point, normal = cam.rayCast(
                    location,
                    cam.worldPosition,
                    speaker.getDistanceTo(cam),
                    xray=False
                )
                occluded = self.occluded = False
                penetration = 1
                while occluder:
                    if occluder is speaker:
                        break
                    sound_occluder = occluder.blenderObject.get(
                        'sound_occluder',
                        True
                    )
                    if sound_occluder:
                        occluded = self.occluded = True
                        block = occluder.blenderObject.get(
                            'sound_blocking',
                            .1
                        )
                        if penetration > 0:
                            penetration -= block
                        else:
                            penetration = 0
                    occluder, point, normal = occluder.rayCast(
                        location,
                        point,
                        speaker.getDistanceTo(point),
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
        if self.reverb_samples:
            self.reverb_samples.update()

    def stop(self):
        '''TODO: Documentation
        '''
        for sound in self.sounds:
            sound.stop()
