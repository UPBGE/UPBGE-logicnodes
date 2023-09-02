from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXY
from ...enum_types import _enum_vrcontroller_trigger_operators
from ....utilities import update_draw
from bpy.props import EnumProperty


@node_type
class LogicNodeVRController(LogicNodeParameterType):
    bl_idname = "NLGetVRControllerValues"
    bl_label = "VR Controller"
    nl_category = "Input"
    nl_subcat = 'VR'
    nl_module = 'parameters'
    index: EnumProperty(
        name='Controller',
        items=_enum_vrcontroller_trigger_operators,
        default='0',
        update=update_draw
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "index", text="")

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_output(NodeSocketLogicVectorXYZ, "Position")
        self.add_output(NodeSocketLogicVectorXYZ, "Orientation")
        self.add_output(NodeSocketLogicVectorXYZ, "Aim Position")
        self.add_output(NodeSocketLogicVectorXYZ, "Aim Orientation")
        self.add_output(NodeSocketLogicVectorXY, "Aim Orientation")
        self.add_output(NodeSocketLogicFloat, "Aim Orientation")

    def get_netlogic_class_name(self):
        return "ULGetVRControllerValues"

    def get_attributes(self):
        return [("index", lambda: f'{self.index}')]

    def get_output_names(self):
        return ['POS', 'ORI', 'APOS', 'AORI', 'STICK', 'TRIGGER']
