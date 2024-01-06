from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from bpy.props import EnumProperty


_vec_sizes = [
    ('0', '2 Dimensional', ''),
    ('1', '3 Dimensional', ''),
    ('2', '4 Dimensional', '')
]


@node_type
class LogicNodeResizeVector(LogicNodeParameterType):
    bl_idname = "LogicNodeResizeVector"
    bl_label = "Resize Vector"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ResizeVectorNode"

    to_size: EnumProperty(
        items=_vec_sizes,
        name='Resize To',
        description='Select the target size of the vector'
    )

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, "Vector")
        self.add_output(NodeSocketLogicVectorXYZ, 'Vector')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'to_size', text='')

    def get_attributes(self):
        return [("to_size", self.to_size)]

    def get_input_names(self):
        return ["vec_in"]

    def get_output_names(self):
        return ['OUT']
