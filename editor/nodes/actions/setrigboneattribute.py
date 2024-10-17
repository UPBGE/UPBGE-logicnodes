from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicArmature
from ...sockets import NodeSocketLogicBone
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicBoolean
from bpy.props import EnumProperty


_attrs = [
    ("name", "Name", "Name of the Bone"),  # String
    None,
    ("head", "Head", "Location of head end of the bone relative to its parent"),  # Vector
    ("head_local", "Local Head", "Location of head end of the bone relative to armature"),  # Vector
    ("tail", "Tail", "Location of tail end of the bone relative to its parent"),  # Vector
    ("tail_local", "Local Tail", "Location of tail end of the bone relative to armature"),  # Vector
    None,
    ("inherit_scale", "Inherit Scale", "Specifies how the bone inherits scaling from the parent bone"),  # Enum
    ("inherit_rotation", "Inherit Rotation", "Bone inherits rotation or scale from parent bone"),  # Boolean
    None,
    ("connected", "Connected", "When bone has a parent, bone's head is stuck to the parent's tail"),  # Boolean
    ("deform", "Deform", "Enable Bone to deform geometry"),  # Boolean
    ("local_location", "Use Local", "Bone location is set in local space"),  # Boolean
    ("relative_parent", "Use Relative Parent", "Object children will use relative transform, like deform"),  # Boolean
    ("scale_easing", "Scale Easing", "Multiply the final easing values by the Scale In/Out Y factors"),  # Boolean
]


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
        elif attr in ['head', 'head_local', 'tail', 'tail_local']:
            self.inputs[3].enabled = False
            self.inputs[4].enabled = True
            self.inputs[5].enabled = False
        else:
            self.inputs[3].enabled = False
            self.inputs[4].enabled = False
            self.inputs[5].enabled = True

    attribute: EnumProperty(items=_attrs, name='Attribute', update=update_draw)
    scale_mode: EnumProperty(items=_scale_modes, name='Scale Mode', update=update_draw)

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'attribute', text='')
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
