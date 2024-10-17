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
    bl_description = 'Three-component ordered structure'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULEuler"

    euler_order: EnumProperty(items=_enum_euler_orders, name='Euler Order')

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, 'X', 'input_x')
        self.add_input(NodeSocketLogicFloat, 'Y', 'input_y')
        self.add_input(NodeSocketLogicFloat, 'Z', 'input_z')
        self.add_output(NodeSocketLogicVectorXYZ, "Euler", 'OUTV')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'euler_order', text='')

    def get_attributes(self):
        return [('order', repr(self.euler_order))]

    # XXX Remove for 5.0
    def get_input_names(self):
        return ["input_x", "input_y", "input_z"]

    # XXX Remove for 5.0
    def get_output_names(self):
        return ["OUTV"]
