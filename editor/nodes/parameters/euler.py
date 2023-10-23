from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXYZ
from ...enum_types import _enum_euler_orders
from bpy.props import EnumProperty


@node_type
class LogicNodeEuler(LogicNodeParameterType):
    bl_idname = "NLParameterEulerSimpleNode"
    bl_label = "Euler"
    nl_module = 'uplogic.nodes.parameters'

    euler_order: EnumProperty(items=_enum_euler_orders)

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, 'X')
        self.add_input(NodeSocketLogicFloat, 'Y')
        self.add_input(NodeSocketLogicFloat, 'Z')
        self.add_output(NodeSocketLogicVectorXYZ, "Euler")
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'euler_order', text='')

    nl_class = "ULEuler"

    def get_output_names(self):
        return ["OUTV"]

    def get_attributes(self):
        return [('order', f'"{self.euler_order}"')]

    def get_input_names(self):
        return ["input_x", "input_y", "input_z"]
