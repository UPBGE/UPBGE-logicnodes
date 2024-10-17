from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from bpy.props import EnumProperty


_vec_sizes = [
    ('0', '2D Vector', ''),
    ('1', '3D Vector', ''),
    ('2', '4D Vector', '')
]


@node_type
class LogicNodeResizeVector(LogicNodeParameterType):
    bl_idname = "LogicNodeResizeVector"
    bl_label = "Resize Vector"
    bl_description = 'Add or remove dimensions of a vector'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ResizeVectorNode"

    to_size: EnumProperty(
        items=_vec_sizes,
        name='Resize To',
        description='Select the target size of the vector'
    )

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, "Vector", 'vec_in')
        self.add_output(NodeSocketLogicVectorXYZ, 'Vector', 'OUT')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'to_size', text='')

    def get_attributes(self):
        return [("to_size", self.to_size)]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["vec_in"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
