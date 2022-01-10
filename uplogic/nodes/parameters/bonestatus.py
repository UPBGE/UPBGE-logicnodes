from bge import logic
from mathutils import Euler
from mathutils import Quaternion
from mathutils import Vector
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import NO_VALUE
from uplogic.utils import is_invalid


class ULBoneStatus(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.armature = None
        self.bone_name = None
        self._prev_armature = NO_VALUE
        self._prev_bone = NO_VALUE
        self._channel = None
        self._pos = Vector((0, 0, 0))
        self._rot = Euler((0, 0, 0), "XYZ")
        self._sca = Vector((0, 0, 0))
        self.XYZ_POS = ULOutSocket(self, self._get_pos)
        self.XYZ_ROT = ULOutSocket(self, self._get_rot)
        self.XYZ_SCA = ULOutSocket(self, self._get_sca)

    def _get_pos(self):
        return self._pos

    def _get_sca(self):
        return self._sca

    def _get_rot(self):
        return self._rot

    def evaluate(self):
        armature = self.get_input(self.armature)
        bone_name = self.get_input(self.bone_name)
        if is_invalid(armature, bone_name):
            return
        self._set_ready()
        channel = None
        if (
            (armature is self._prev_armature) and
            (bone_name == self._prev_bone)
        ):
            channel = self._channel
        else:
            self._prev_armature = armature
            self._prev_bone = bone_name
            self._channel = armature.channels[bone_name]
            channel = self._channel
        if channel.rotation_mode is logic.ROT_MODE_QUAT:
            self._rot[:] = (
                Quaternion(channel.rotation_quaternion).to_euler()
            )
        else:
            self._rot[:] = channel.rotation_euler
        self._pos[:] = channel.location
        self._sca[:] = channel.scale
