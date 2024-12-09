from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicArmature
from ...sockets import NodeSocketLogicBone
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicVectorXYZAngle
from ...sockets import NodeSocketLogicBoolean
from ...enum_types import _bone_attrs
from bpy.props import EnumProperty
from bpy.props import BoolProperty


@node_type
class LogicNodeGetRigBoneAttribute(LogicNodeParameterType):
    bl_idname = "LogicNodeGetRigBoneAttribute"
    bl_label = "Get Bone Attribute"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "GetRigBoneAttributeNode"
    bl_description = 'Get an attribute of an armature bone'

    _labels = {
        "name": 'Get Bone Name',
        "location": 'Get Bone Location',
        "pose_rotation_euler": 'Get Bone Euler Rotation',
        "head": 'Get Bone Head',
        "head_local": 'Get Bone Local Head',
        "head_pose": 'Get Bone Pose Head',
        "center": 'Get Bone Center',
        "center_local": 'Get Bone Local Center',
        "center_pose": 'Get Bone Pose Center',
        "tail": 'Get Bone Tail',
        "tail_pose": 'Get Bone Local Tail',
        "tail_local": 'Get Bone Pose Tail',
        "inherit_scale": 'Get Bone Inherit Scale',
        "inherit_rotation": 'Get Bone Inherit Rotation',
        "connected": 'Get Bone Connected',
        "deform": 'Get Bone Deform',
        "use_local_location": 'Get Bone Local',
        "use_relative_parent": 'Get Bone Relative Parent',
        "use_scale_easing": 'Get Bone Scale Easing'
    }

    def update_draw(self, context=None):
        attr = self.attribute
        if attr == 'inherit_scale':
            self.set_socket_state(self.outputs[0], True, 'Mode')
            self.outputs[1].enabled = False
            self.outputs[2].enabled = False
            self.outputs[3].enabled = False
        elif attr == 'name':
            self.set_socket_state(self.outputs[0], True, 'Name')
            self.outputs[1].enabled = False
            self.outputs[2].enabled = False
            self.outputs[3].enabled = False
        elif attr in [
            'head',
            'head_local',
            'head_pose',
            'tail',
            'tail_local',
            'tail_pose',
            'center',
            'center_local',
            'center_pose',
            'location'
        ]:
            self.outputs[0].enabled = False
            self.outputs[1].enabled = True
            self.outputs[2].enabled = False
            self.outputs[3].enabled = False
        elif attr in [
            'pose_rotation_euler'
        ]:
            self.outputs[0].enabled = False
            self.outputs[1].enabled = False
            self.outputs[2].enabled = True
            self.outputs[3].enabled = False
        else:
            self.outputs[0].enabled = False
            self.outputs[1].enabled = False
            self.outputs[2].enabled = False
            self.outputs[3].enabled = True
        self.nl_label = self._labels[attr]

    attribute: EnumProperty(items=_bone_attrs, name='Attribute', update=update_draw)
    world_space: BoolProperty(name='World Space')

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'attribute', text='')
        if self.attribute in [
            'head',
            'head_local',
            'head_pose',
            'tail',
            'tail_local',
            'tail_pose',
            'center',
            'center_local',
            'center_pose'
        ]:
            layout.prop(self, 'world_space', text='Use World Space')

    def get_attributes(self):
        return [
            ('attribute', repr(self.attribute)),
            ('world_space', repr(self.world_space))
        ]

    def init(self, context):
        self.add_input(NodeSocketLogicArmature, "", 'armature')
        self.add_input(NodeSocketLogicBone, "", 'bone', settings={'ref_index': 0})
        self.add_output(NodeSocketLogicString, "", 'VALUE')
        self.add_output(NodeSocketLogicVectorXYZ, "Vector", 'VALUE')
        self.add_output(NodeSocketLogicVectorXYZAngle, "Rotation", 'VALUE')
        self.add_output(NodeSocketLogicBoolean, "Bool", 'VALUE')
        LogicNodeParameterType.init(self, context)
