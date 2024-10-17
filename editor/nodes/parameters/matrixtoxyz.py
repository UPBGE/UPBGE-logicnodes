from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicMatrix
from ...sockets import NodeSocketLogicVectorXYZ
from ...enum_types import _enum_vector_types
from ...enum_types import _enum_euler_orders
from bpy.props import EnumProperty


@node_type
class LogicNodeMatrixToXYZ(LogicNodeParameterType):
    bl_idname = "NLParameterMatrixToEulerNode"
    bl_label = "Matrix To XYZ"
    bl_description = 'Convert a matrix to a 3D vector or Euler'
    bl_width_default = 200
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULMatrixToXYZ"

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.outputs[-1].name = 'Euler' if int(self.output) else 'Vector'

    output: EnumProperty(
        name='XYZ Type',
        items=_enum_vector_types,
        description="Output",
        update=update_draw
    )

    euler_order: EnumProperty(
        items=_enum_euler_orders,
        name='Euler Order'
    )

    def init(self, context):
        self.add_input(NodeSocketLogicMatrix, 'Matrix', 'input_m')
        self.add_output(NodeSocketLogicVectorXYZ, "XYZ", 'OUT')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "output", text='')
        if int(self.output) == 1:
            layout.prop(self, "euler_order", text='')

    def get_attributes(self):
        return [("output", self.output), ("euler_order", repr(self.euler_order))]

    # XXX Remove for 5.0
    def get_input_names(self):
        return ["input_m"]

    # XXX Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
