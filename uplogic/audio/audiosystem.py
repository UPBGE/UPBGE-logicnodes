'''TODO: Documentation
'''

from bge import logic
from uplogic.data.globaldb import GlobalDB
import aud
import bpy


DISTANCE_MODELS = {
    'EXPONENT': aud.DISTANCE_MODEL_EXPONENT,
    'EXPONENT_CLAMPED': aud.DISTANCE_MODEL_EXPONENT_CLAMPED,
    'INVERSE': aud.DISTANCE_MODEL_INVERSE,
    'INVERSE_CLAMPED': aud.DISTANCE_MODEL_INVERSE_CLAMPED,
    'LINEAR': aud.DISTANCE_MODEL_LINEAR,
    'LINEAR_CLAMPED': aud.DISTANCE_MODEL_LINEAR_CLAMPED,
    'NONE': aud.DISTANCE_MODEL_INVALID
}


class ULAudioSystem(object):
    '''TODO: Documentation
    '''
    def __init__(self, name: str):
        self.active_sounds = []
        scene = logic.getCurrentScene()
        self.listener = scene.active_camera
        self.old_lis_pos = self.listener.worldPosition.copy()
        self.device = aud.Device()
        self.device.distance_model = aud.DISTANCE_MODEL_INVERSE_CLAMPED
        self.device.speed_of_sound = bpy.context.scene.audio_doppler_speed
        self.device.doppler_factor = bpy.context.scene.audio_doppler_factor
        GlobalDB.retrieve('uplogic.audio').put(name, self)
        bpy.app.handlers.game_post.append(self.shutdown)
        scene.pre_draw.append(self.update)

    def get_distance_model(self, name):
        return DISTANCE_MODELS.get(name, aud.DISTANCE_MODEL_INVERSE_CLAMPED)

    def compute_listener_velocity(self, listener):
        wpos = listener.worldPosition.copy()
        olp = self.old_lis_pos
        vel = (
            (wpos.x - olp.x) * 50,
            (wpos.y - olp.y) * 50,
            (wpos.z - olp.z) * 50
        )
        self.old_lis_pos = wpos
        return vel

    def update(self, cam):
        self.listener = cam
        if not self.active_sounds:
            return  # do not update if no sound has been installed
        # update the listener data
        dev = self.device
        listener_vel = self.compute_listener_velocity(cam)
        dev.listener_location = cam.worldPosition
        dev.listener_orientation = cam.worldOrientation.to_quaternion()
        dev.listener_velocity = listener_vel
        for s in self.active_sounds:
            s.update()

    def add(self, sound):
        self.active_sounds.append(sound)

    def remove(self, sound):
        self.active_sounds.remove(sound)

    def shutdown(self, a, b):
        self.device.stopAll()
        bpy.app.handlers.game_post.remove(self.shutdown)
