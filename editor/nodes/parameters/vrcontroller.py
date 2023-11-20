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
    nl_module = 'uplogic.nodes.parameters'

    index: EnumProperty(
        name='Controller',
        items=_controllers,
        default='0'
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "index", text="")

    def init(self, context):
        self.add_output(NodeSocketLogicVectorXYZ, "Position")
        self.add_output(NodeSocketLogicVectorXYZ, "Orientation")
        self.add_output(NodeSocketLogicVectorXYZ, "Aim Position")
        self.add_output(NodeSocketLogicVectorXYZ, "Aim Orientation")
        self.add_output(NodeSocketLogicVectorXY, "Stick")
        self.add_output(NodeSocketLogicFloat, "Trigger")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULGetVRControllerValues"

    def get_attributes(self):
        return [("index", f'{self.index}')]

    def get_output_names(self):
        return ['POS', 'ORI', 'APOS', 'AORI', 'STICK', 'TRIGGER']
