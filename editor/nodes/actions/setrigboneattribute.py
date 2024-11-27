from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicArmature
from ...sockets import NodeSocketLogicBone
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicBoolean
from ...enum_types import _set_bone_attrs
from bpy.props import EnumProperty


_scale_modes = [
    ("NONE", "None", "Completely ignore parent scaling"),
    ("FULL", "Full", "Inherit all effects of parent scaling."),
    None,
    ("NONE_LEGACY", "None (Legacy)", "Ignore parent scaling without compensating for parent shear. Replicates the effect of disabling the original Inherit Scale checkbox"),
    ("FIX_SHEAR", "Fix Shear", "Inherit scaling, but remove shearing of the child in the rest orientation"),
    ("ALIGNED", "Aligned", "Rotate non-uniform parent scaling to align with the child, applying parent X scale to child X axis, and so forth"),
    ("AVERAGE", "Average", "Inherit uniform scaling representing the overall change in the volume of the parent")
]


@node_type
class LogicNodeSetRigBoneAttribute(LogicNodeActionType):
    bl_idname = "LogicNodeSetRigBoneAttribute"
    bl_label = "Set Bone Attribute"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "SetRigBoneAttributeNode"
    bl_description = 'Set an attribute of an armature bone'

    def update_draw(self, context=None):
        attr = self.attribute
        if attr == 'inherit_scale':
            self.inputs[3].enabled = False
            self.inputs[4].enabled = False
            self.inputs[5].enabled = False
        elif attr == 'name':
            self.inputs[3].enabled = True
            self.inputs[4].enabled = False
            self.inputs[5].enabled = False
        elif attr in [
            'location',
        ]:
            self.inputs[3].enabled = False
            self.inputs[4].enabled = True
            self.inputs[5].enabled = False
        else:
            self.inputs[3].enabled = False
            self.inputs[4].enabled = False
            self.inputs[5].enabled = True

    attribute: EnumProperty(items=_set_bone_attrs, name='Attribute', update=update_draw)
    scale_mode: EnumProperty(items=_scale_modes, name='Scale Mode', update=update_draw)

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'attribute', text='')
        # if self.attribute in [
        #     'location'
        # ]:
        #     layout.prop(self, 'world_space', text='')
        if self.attribute == 'inherit_scale':
            layout.prop(self, 'scale_mode', text='')

    def get_attributes(self):
        return [
            ('attribute', repr(self.attribute)),
            ('scale_mode', repr(self.scale_mode))
        ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicArmature, "", 'armature')
        self.add_input(NodeSocketLogicBone, "", 'bone', settings={'ref_index': 1})
        self.add_input(NodeSocketLogicString, "", 'value')
        self.add_input(NodeSocketLogicVectorXYZ, "Vector", 'value')
        self.add_input(NodeSocketLogicBoolean, "Bool", 'value')
        self.add_output(NodeSocketLogicCondition, 'Done', 'DONE')
        LogicNodeActionType.init(self, context)
