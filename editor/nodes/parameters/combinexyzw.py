from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeCombineXYZW(LogicNodeParameterType):
    bl_idname = "NLParameterVector4SimpleNode"
    bl_label = "Combine XYZW"
    bl_description = 'Four-dimensional vector'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULVectorXYZW"

    search_tags = [
        ['Combine XYZW', {}],
        ['Vector XYZW', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, 'X', 'input_x')
        self.add_input(NodeSocketLogicFloat, 'Y', 'input_y')
        self.add_input(NodeSocketLogicFloat, 'Z', 'input_z')
        self.add_input(NodeSocketLogicFloat, 'W', 'input_w')
        self.add_output(NodeSocketLogicVectorXYZ, "Vector", 'OUTV')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUTV"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["input_x", "input_y", "input_z", 'input_w']
