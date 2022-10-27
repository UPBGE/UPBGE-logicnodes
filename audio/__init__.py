import aud
import bpy
from os.path import isfile
from mathutils import Euler, Vector

SYSTEM = None


DISTANCE_MODELS = {
    'EXPONENT': aud.DISTANCE_MODEL_EXPONENT,
    'EXPONENT_CLAMPED': aud.DISTANCE_MODEL_EXPONENT_CLAMPED,
    'INVERSE': aud.DISTANCE_MODEL_INVERSE,
    'INVERSE_CLAMPED': aud.DISTANCE_MODEL_INVERSE_CLAMPED,
    'LINEAR': aud.DISTANCE_MODEL_LINEAR,
    'LINEAR_CLAMPED': aud.DISTANCE_MODEL_LINEAR_CLAMPED,
    'NONE': aud.DISTANCE_MODEL_INVALID
}


class ViewportCamera(object):

    def __init__(self):
        pass

    @property
    def view(self):
        for a in bpy.context.window.screen.areas:
            if a.type == 'VIEW_3D':
                return a.spaces[0]
    #     """ Returns the set of 3D views.
    #     """
    #     rtn = []
    #     for a in self.context.window.screen.areas:
    #         if a.type == 'VIEW_3D':
    #             rtn.append(a)
    #     return rtn

    # def camera(self, view):
    #     """ Return position, rotation data about a given view for the first space attached to it """
    #     look_at = view.spaces[0].region_3d.view_location
    #     camera_pos = self.camera_position(matrix)
    #     rotation = view.spaces[0].region_3d.view_rotation
    #     return look_at, camera_pos, rotation

    @property
    def location(self):
        matrix = self.view.region_3d.view_matrix
        """ From 4x4 matrix, calculate camera location """
        t = (matrix[0][3], matrix[1][3], matrix[2][3])
        r = (
            (matrix[0][0], matrix[0][1], matrix[0][2]),
            (matrix[1][0], matrix[1][1], matrix[1][2]),
            (matrix[2][0], matrix[2][1], matrix[2][2])
        )
        rp = (
            (-r[0][0], -r[1][0], -r[2][0]),
            (-r[0][1], -r[1][1], -r[2][1]),
            (-r[0][2], -r[1][2], -r[2][2])
        )
        output = (
            rp[0][0] * t[0] + rp[0][1] * t[1] + rp[0][2] * t[2],
            rp[1][0] * t[0] + rp[1][1] * t[1] + rp[1][2] * t[2],
            rp[2][0] * t[0] + rp[2][1] * t[1] + rp[2][2] * t[2],
        )
        return Vector(output)
    
    @property
    def orientation(self):
        return self.view.region_3d.view_rotation


class NLAudioSystem(object):
    '''System for managing sounds started using `NLSound2D` or `NLSound3D`.

    This is usually addressed indirectly through `NLSound2D` or `NLSound3D` and
    is not intended for manual use.
    '''

    def __init__(self, name: str, mode: str = '3D'):
        self.active_sounds = []
        self.name = name
        self.mode = mode
        self.bounces = 0
        self.volume = 1.0
        self.reverb = False
        self._lowpass = False
        self.device = aud.Device()
        self.device.distance_model = DISTANCE_MODELS[bpy.context.scene.audio_distance_model]
        self.device.speed_of_sound = bpy.context.scene.audio_doppler_speed
        self.device.doppler_factor = bpy.context.scene.audio_doppler_factor
        self.reverb_volumes = []
        self.scene = bpy.context.scene
        self.listener = ViewportCamera()
        # self.use_vr = getattr(bpy.data.scenes[self.scene.name], 'use_vr_audio_space', False)
        # self.vr_headset = ULHeadsetVRWrapper() if check_vr_session_status() else None
        # self.listener = self.scene.camera
        self.old_lis_pos = self.listener.location
        self.setup(self.scene)
        self.get_speakers()
        # NLSound3D(
        #     self.scene.objects['Cube'], 'C:/Users/Zedikon/Music/Ghetto Blastah (Original Mix).wav')
        # self.scene.onRemove.append(self.shutdown)

    @property
    def lowpass(self):
        return self._lowpass

    @lowpass.setter
    def lowpass(self, val):
        if val == self._lowpass:
            return
        self._lowpass = val
        for sound in self.active_sounds:
            sound.lowpass = val

    def get_speakers(self):
        for obj in self.scene.objects:
            if 'volume' in dir(obj.data):
                NLSound3D(
                    obj,
                    obj.data.sound.filepath,
                    False,
                    .1,
                    .1,
                    -1,
                    obj.data.pitch,
                    obj.data.volume,
                    False,
                    obj.data.attenuation,
                    obj.data.distance_reference,
                    [obj.data.cone_angle_inner, obj.data.cone_angle_outer],
                    obj.data.cone_volume_outer
                )

    def setup(self, scene=None):
        """Get necessary scene data.
        """
        if scene is None:
            self.scene = bpy.context.scene
        else:
            self.scene = scene
        for obj in self.scene.objects:
            if getattr(obj, 'reverb_volume', False) and not obj.data:
                self.reverb_volumes.append(obj)
        self.reverb = len(self.reverb_volumes) > 0
        global SYSTEM
        SYSTEM = self

    def get_distance_model(self, name):
        return DISTANCE_MODELS.get(name, aud.DISTANCE_MODEL_INVERSE_CLAMPED)

    def compute_listener_velocity(self, listener):
        """Compare positions of the listener to calculate velocity.
        """
        wpos = listener.location
        olp = self.old_lis_pos
        vel = (
            (wpos.x - olp.x) * 50,
            (wpos.y - olp.y) * 50,
            (wpos.z - olp.z) * 50
        )
        self.old_lis_pos = wpos
        return vel

    def update(self):
        """This is called each frame.
        """
        if self.mode == '3D':
            scene = bpy.context.scene
            if scene is not self.scene:
                self.setup(scene)
            # listener = scene.camera
            listener = self.listener
            self.reverb = False
            # if not self.use_vr:
            # self.listener = listener
            if not self.active_sounds:
                return  # do not update if no sound has been installed
            # update the listener data
            cpos = listener.location
            distances = {}
            # if self.reverb_volumes:
            #     for obj in self.reverb_volumes:
            #         dist = (obj.location - cpos).length
            #         if dist > 50:
            #             continue
            #         else:
            #             distances[dist] = obj
            #     min_dist = distances[min(distances.keys())]
            #     obj = min_dist
            #     r = obj.empty_display_size
            #     wpos = obj.location
            #     sca = obj.scale
            #     # if cam.getDistanceTo(obj) < ob.empty_display_size:
            #     in_range = (
            #         wpos.x - r*sca.x < cpos.x < wpos.x + r*sca.x and
            #         wpos.y - r*sca.y < cpos.y < wpos.y + r*sca.y and
            #         wpos.z - r*sca.z < cpos.z < wpos.z + r*sca.z
            #     )
            #     if in_range:
            #         self.reverb = True
            #         self.bounces = obj.reverb_samples
            # listener_vel = self.compute_listener_velocity(listener)
            dev = self.device
            dev.listener_location = cpos
            dev.listener_orientation = listener.orientation
            # dev.listener_velocity = listener_vel
        for s in self.active_sounds:
            s.update()

    def add(self, sound):
        '''Add a `ULSound` to this audio system.'''
        self.active_sounds.append(sound)

    def remove(self, sound):
        '''Remove a `ULSound` from this audio system.'''
        self.active_sounds.remove(sound)

    def shutdown(self, a=None):
        '''Stop and remove this audio system. This will stop all sounds playing
        on this system.'''
        self.device.stopAll()
        global SYSTEM
        SYSTEM = None


def get_audio_system(system_name: str = 'default', mode: str = '3D') -> NLAudioSystem:
    '''Get or create a `ULAudioSystem` with the given name.

    :param `system_name`: Look for this name.

    :returns: `ULAudioSystem`, new system is created if none is found.
    '''
    global SYSTEM
    aud_sys = SYSTEM
    if aud_sys is None:
        aud_sys = NLAudioSystem(system_name, mode)
    return aud_sys


class NLSound():
    """Base class for 2D and 3D Sounds
    """

    sound = None
    """Internal `aud.Sound` instance."""
    finished: bool
    """Whether this sound has finished playing."""
    pitch: float
    """Pitch (Frequency Shift)."""
    volume: float
    aud_system: NLAudioSystem

    @property
    def position(self):
        if self.sound:
            return self.sound.position

    @position.setter
    def position(self, val):
        if self.sound:
            self.sound.position = val

    def stop(self):
        '''TODO: Documentation
        '''
        self.sound.stop()

    def pause(self):
        self.sound.pause()

    def resume(self):
        self.sound.resume()


class NLSound2D(NLSound):
    '''Non-spacial sound, e.g. Music or Voice-Overs.\n
    This class allows for modification of pitch and volume while playing.

    :param `file`: Path to the sound file.
    :param `volume`: Initial volume.
    :param `pitch`: Initial pitch.
    :param `loop_count`: Plays the sound this many times (0 for once, -1 for endless).
    :param `aud_sys`: Audiosystem to play this sound on.
    '''

    sound: aud.Handle

    def __init__(
        self,
        file: str = '',
        volume: float = 1,
        pitch: float = 1,
        loop_count: int = 0,
        lowpass=False,
        aud_sys: str = 'default'
    ):
        self.file = file
        self._volume = 1
        self.finished = False
        if not (file):
            return
        self.aud_system = get_audio_system(aud_sys)
        soundfile = bpy.path.abspath(file)
        if not isfile(file):
            print(f'Soundfile {file} could not be loaded!')
            return
        sound = self.soundfile = aud.Sound(file)
        lowpass = self.aud_system.lowpass or lowpass
        if lowpass:
            sound = self.soundfile = sound.lowpass(lowpass, .5)
        device = self.aud_system.device
        self.sound = handle = device.play(sound)

        handle.relative = True
        handle.loop_count = loop_count
        self.aud_system.add(self)
        self.volume = volume
        self.pitch = pitch
        self._lowpass = False
        self.lowpass = self.aud_system.lowpass

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, val):
        if self.sound and self.sound.status:
            self.sound.volume = val * self.aud_system.volume
        self._volume = val

    @property
    def pitch(self):
        if self.sound and self.sound.status:
            return self.sound.pitch

    @pitch.setter
    def pitch(self, val):
        if self.sound and self.sound.status:
            self.sound.pitch = val

    # @property
    # def lowpass(self):
    #     return self._lowpass

    # @lowpass.setter
    # def lowpass(self, val):
    #     if self._lowpass == val:
    #         return
    #     self._lowpass = val
    #     sound = self.soundfile
    #     if val:
    #         sound = sound.lowpass(val, .5)
    #     sound = self.aud_system.device.play(sound)
    #     sound.loop_count = self.sound.loop_count
    #     sound.position = self.sound.position
    #     sound.volume = self.sound.volume
    #     sound.pitch = self.sound.pitch
    #     schedule_callback(self.sound.stop, .1)
    #     self.sound = sound

    def update(self):
        '''TODO: Documentation
        '''
        if self.volume == 0:
            return
        handle = self.sound
        if not handle.status:
            self.finished = True
            self.aud_system.remove(self)
            return


class NLSound3D(NLSound):
    '''Spacial sound, e.g. World Effects or Voices.\n
    This class allows for modification of pitch and volume as well as other attributes while playing.
    '''

    def __init__(
        self,
        speaker: bpy.types.Object = None,
        file: str = '',
        occlusion: bool = False,
        transition_speed: float = .1,
        cutoff_frequency: float = .1,
        loop_count: int = 0,
        pitch: float = 1,
        volume: float = 1,
        reverb=False,
        attenuation: float = 1,
        distance_ref: float = 1,
        cone_angle: list[float] = [360, 360],
        cone_outer_volume: float = 0,
        aud_sys: str = 'default'
    ):
        self.file = file
        self.finished = False
        if not (file and speaker):
            return
        self._clear_sound = 1
        self._sustained = 1
        self.occluded = False
        self.sounds = []
        self.reverb_samples = None
        self.aud_system = get_audio_system(aud_sys)
        self.speaker = speaker
        self.reverb = reverb
        self.occlusion = occlusion
        self.volume = volume
        self.pitch = pitch
        self.cone_outer_volume = cone_outer_volume
        master_volume = self.aud_system.volume
        self.transition = transition_speed
        file = bpy.path.abspath(file)
        if not isfile(file):
            print(f'Soundfile {file} could not be loaded!')
            return
        sound = self.soundpath = aud.Sound(file).rechannel(1)
        device = self.aud_system.device
        handle = device.play(sound)
        if occlusion:
            soundlow = aud.Sound.lowpass(
                sound, 4400 * cutoff_frequency, .5).rechannel(1)
            handlelow = device.play(soundlow)
            self.handles = [speaker, [handle, handlelow]]
        else:
            self.handles = [speaker, [handle]]
        for handle in self.handles[1]:
            handle.relative = False
            handle.location = speaker.location
            handle.attenuation = attenuation
            handle.orientation = speaker.rotation_quaternion
            handle.pitch = pitch
            handle.volume = volume * master_volume
            handle.distance_reference = distance_ref
            handle.distance_maximum = 1000
            handle.cone_angle_inner = cone_angle[0]
            handle.cone_angle_outer = cone_angle[1]
            handle.loop_count = loop_count
            handle.cone_volume_outer = cone_outer_volume * volume * master_volume
        self.aud_system.add(self)

    def update(self):
        '''TODO: Documentation
        '''
        if self.volume == 0:
            for i, handle in enumerate(self.handles[1]):
                handle.volume = 0
            return
        aud_system = self.aud_system
        speaker = self.speaker
        if speaker is None or speaker.name not in bpy.context.scene.objects:
            self.finished = True
            aud_system.remove(self)
            return
        location = speaker.location
        for i, handle in enumerate(self.handles[1]):
            if not handle.status:
                self.finished = True
                aud_system.remove(self)
                return
            handle.pitch = self.pitch
            handle.location = location
            handle.orientation = (
                speaker
                .rotation_quaternion
            )
            handle.velocity = Vector((0, 0, 0))
            mult = 1.0
            # if self.occlusion:
            #     transition = self.transition
            #     cam = self.aud_system.listener
            #     occluder, point, normal = cam.ray_cast(
            #         location,
            #         cam.location,
            #         speaker.getDistanceTo(cam.worldPosition),
            #         xray=False
            #     )
            #     occluded = self.occluded = False
            #     penetration = 1
            #     while occluder:
            #         if occluder is speaker:
            #             break
            #         sound_occluder = occluder.blenderObject.get(
            #             'sound_occluder',
            #             True
            #         )
            #         if sound_occluder:
            #             occluded = self.occluded = True
            #             block = occluder.blenderObject.get(
            #                 'sound_blocking',
            #                 .1
            #             )
            #             if penetration > 0:
            #                 penetration -= block
            #             else:
            #                 penetration = 0
            #         occluder, point, normal = occluder.rayCast(
            #             location,
            #             point,
            #             speaker.getDistanceTo(point),
            #             xray=False
            #         )
            #     cs = self._clear_sound
            #     if occluded and cs > 0:
            #         self._clear_sound -= transition
            #     elif not occluded and cs < 1:
            #         self._clear_sound += transition
            #     if self._clear_sound < 0:
            #         self._clear_sound = 0
            #     sustained = self._sustained
            #     if sustained > penetration:
            #         self._sustained -= transition / 10
            #     elif sustained < penetration:
            #         self._sustained += transition / 10
            #     mult = (
            #         cs * sustained
            #         if not i
            #         else (1 - cs) * sustained
            #     )
            master_volume = self.aud_system.volume
            handle.volume = self.volume * mult * master_volume
            handle.cone_volume_outer = (
                self.cone_outer_volume *
                self.volume *
                mult *
                master_volume
            )

    def stop(self):
        '''TODO: Documentation
        '''
        for sound in self.sounds:
            sound.stop()
