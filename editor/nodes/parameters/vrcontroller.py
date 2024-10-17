from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXY
from bpy.props import EnumProperty



_controllers = [
    ("0", "Left", "Left Controller Values"),
    ("1", "Right", "Right Controller Values")
]


@node_type
class LogicNodeVRController(LogicNodeParameterType):
    bl_idname = "NLGetVRControllerValues"
    bl_label = "VR Controller"
    bl_description = 'World space date of a VR controller'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetVRControllerValues"

    index: EnumProperty(
        name='Controller',
        items=_controllers,
        default='0'
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "index", text="")

    def init(self, context):
        self.add_output(NodeSocketLogicVectorXYZ, "Position", 'POS')
        self.add_output(NodeSocketLogicVectorXYZ, "Orientation", 'ORI')
        self.add_output(NodeSocketLogicVectorXYZ, "Aim Position", 'APOS')
        self.add_output(NodeSocketLogicVectorXYZ, "Aim Orientation", 'AORI')
        self.add_output(NodeSocketLogicVectorXY, "Stick", 'STICK')
        self.add_output(NodeSocketLogicFloat, "Trigger", 'TRIGGER')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_attributes(self):
        return [("index", f'{self.index}')]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['POS', 'ORI', 'APOS', 'AORI', 'STICK', 'TRIGGER']
