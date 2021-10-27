'''TODO: Documentation
'''

from bge import logic
from bge.types import KX_GameObject as GameObject
from mathutils import Vector
from uplogic.audio import ULAudioSystem, audiosystem
from uplogic.data import GlobalDB
from uplogic.utils import compute_distance
from uplogic.utils import interpolate
import aud
import time


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
    sounds = []
    reverbs = []
    speaker: GameObject
    occlusion: bool
    cone_outer_volume: float
    transition: float
    soundpath: str
    reverb: bool
    room_scale: float
    r_time = time.time()
    _clear_sound: float = 1
    _sustained: float = 1

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
        loop_count: int = 1,
        reverb=False,
        bounces=10
    ):
        if not (file and aud_system and speaker):
            return
        self.aud_system = self.get_aud_sys(aud_system)
        self.speaker = speaker
        self.reverb = reverb
        self.bounces = bounces
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
        self.aud_system.add(self)

    def update(self):
        '''TODO: Documentation
        '''
        aud_system = self.aud_system
        speaker = self.speaker
        now = time.time()
        if aud_system.reverb or self.reverb:
            if len(self.reverbs) < 30:
                if now - self.r_time > .1:
                    self.reverbs.append(ULReverb(
                        self,
                        self.soundpath,
                        self.handles[1][0],
                        len(self.reverbs) + 1,
                    ))
                    self.r_time = now
            else:
                self.r_time = now
        elif now - self.r_time > 1 and self.reverbs and not self.reverb:
            for r in self.reverbs:
                r.stop()
            self.reverbs.clear()
        if not speaker:
            self.finished = True
            aud_system.remove(self)
        for i, handle in enumerate(self.handles[1]):
            if not handle.status:
                self.finished = True
                aud_system.remove(self)
                return
            handle.pitch = self.pitch * logic.getTimeScale()
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
        for r in self.reverbs:
            r.update()

    def stop(self):
        '''TODO: Documentation
        '''
        for sound in self.sounds:
            sound.stop()


class ULReverb():

    volume = 0
    mult = 0

    def __init__(
        self,
        parent,
        sound,
        handle,
        idx,
    ):
        self.idx = idx
        self.parent = parent
        self.handle = handle
        self.sound = sound = parent.aud_system.device.play(sound)
        sound.relative = handle.relative
        sound.location = handle.location
        sound.velocity = handle.velocity
        sound.position = handle.position - self.idx/20
        sound.attenuation = handle.attenuation
        sound.orientation = handle.orientation
        sound.pitch = handle.pitch
        sound.volume = 0
        sound.distance_reference = handle.distance_reference
        sound.distance_maximum = handle.distance_maximum
        sound.cone_angle_inner = handle.cone_angle_inner
        sound.cone_angle_outer = handle.cone_angle_outer
        sound.loop_count = handle.loop_count
        sound.cone_volume_outer = handle.cone_volume_outer

    def update(self):
        parent = self.parent
        aud_sys = parent.aud_system
        target_vol = 1 if parent.reverb else aud_sys.reverb
        bounces = parent.bounces if parent.reverb else aud_sys.bounces
        self.volume = interpolate(self.volume, target_vol, .1)
        self.mult = interpolate(self.mult, (1-(self.idx / bounces)) if self.idx < bounces else 0, .1)
        sound = self.sound
        handle = self.handle
        loc = handle.location
        lloc = aud_sys.device.listener_location
        loc = (loc[0]-lloc[0], loc[1]-lloc[1], loc[2]-lloc[2])
        sound.location = (
            -(loc[0]-lloc[0]),
            -(loc[1]-lloc[1]),
            -(loc[2]-lloc[2])
        )
        sound.velocity = handle.velocity
        sound.attenuation = handle.attenuation
        sound.orientation = handle.orientation
        sound.distance_maximum = handle.distance_maximum
        sound.cone_angle_inner = handle.cone_angle_inner
        sound.pitch = handle.pitch
        sound.volume = handle.volume * self.volume * .5 * (self.mult**2)
        sound.cone_volume_outer = handle.cone_volume_outer

    def stop(self):
        self.sound.stop()
