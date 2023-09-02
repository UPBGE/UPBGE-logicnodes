from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicMatrix
from ...sockets import NodeSocketLogicVectorXYZ
from ...enum_types import _enum_vector_types
from ...enum_types import _enum_euler_orders
from ....utilities import update_draw
from bpy.props import EnumProperty


@node_type
class LogicNodeMatrixToXYZ(LogicNodeParameterType):
    bl_idname = "NLParameterMatrixToEulerNode"
    bl_label = "Matrix To XYZ"
    nl_category = "Math"
    bl_width_default = 200
    nl_subcat = 'Vector Math'
    nl_module = 'parameters'

    output: EnumProperty(
        name='XYZ Type',
        items=_enum_vector_types,
        description="Output",
        update=update_draw
    )

    euler_order: EnumProperty(
        items=_enum_euler_orders,
        update=update_draw
    )

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicMatrix, 'Matrix')
        self.add_output(NodeSocketLogicVectorXYZ, "XYZ")

    def get_netlogic_class_name(self):
        return "ULMatrixToXYZ"

    def draw_buttons(self, context, layout):
        layout.prop(self, "output", text='')
        if int(self.output) == 1:
            layout.prop(self, "euler_order", text='')

    def update_draw(self):
        self.outputs[-1].name = 'Euler' if int(self.output) else 'Vector'

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["input_m"]

    def get_attributes(self):
        return [("output", f'{self.output}'), ("euler_order", f'"{self.euler_order}"')]
