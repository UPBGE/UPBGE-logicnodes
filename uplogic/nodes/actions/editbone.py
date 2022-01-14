from bge import logic
from mathutils import Euler
from mathutils import Vector
from mathutils import Quaternion
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULEditBone(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.armature = None
        self.bone_name = None
        self.set_translation = None
        self.set_orientation = None
        self.set_scale = None
        self.translate = None
        self.rotate = None
        self.scale = None
        self._eulers = Euler((0, 0, 0), "XYZ")
        self._vector = Vector((0, 0, 0))
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def _convert_orientation(self, ch, xyzrot):
        eulers = self._eulers
        eulers[:] = xyzrot
        if ch.rotation_mode is logic.ROT_MODE_QUAT:
            return eulers.to_quaternion()
        else:
            return xyzrot

    def _set_orientation(self, ch, rot):
        orientation = self._convert_orientation(ch, rot)
        if ch.rotation_mode is logic.ROT_MODE_QUAT:
            ch.rotation_quaternion = orientation
        else:
            ch.rotation_euler = orientation

    def _rotate(self, ch, xyzrot):
        orientation = self._convert_orientation(ch, xyzrot)
        if ch.rotation_mode is logic.ROT_MODE_QUAT:
            ch.rotation_quaternion = (
                Quaternion(ch.rotation_quaternion) * orientation
            )
        else:
            ch.rotation_euler = ch.rotation_euler.rotate(orientation)

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        armature = self.get_input(self.armature)
        bone_name = self.get_input(self.bone_name)
        set_translation = self.get_input(self.set_translation)
        set_orientation = self.get_input(self.set_orientation)
        set_scale = self.get_input(self.set_scale)
        translate = self.get_input(self.translate)
        rotate = self.get_input(self.rotate)
        scale = self.get_input(self.scale)
        if is_waiting(
            armature,
            bone_name,
            set_translation,
            set_orientation,
            set_scale,
            translate,
            rotate,
            scale
        ):
            return
        self._set_ready()
        if is_invalid(armature):
            return
        if not bone_name:
            return
        # TODO cache the bone index
        bone_channel = armature.channels[bone_name]
        if set_translation is not None:
            bone_channel.location = set_translation
        if set_orientation is not None:
            self._set_orientation(bone_channel, set_orientation)
        if set_scale is not None:
            bone_channel.scale = set_scale
        if translate is not None:
            vec = self._vector
            vec[:] = translate
            bone_channel.location = bone_channel.location + vec
        if scale is not None:
            vec = self._vector
            vec[:] = scale
            bone_channel.scale = bone_channel.scale + vec
        if rotate is not None:
            self._rotate(bone_channel, rotate)
        armature.update()
        self.done = True
