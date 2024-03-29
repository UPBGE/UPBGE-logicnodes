from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeCombineXYZW(LogicNodeParameterType):
    bl_idname = "NLParameterVector4SimpleNode"
    bl_label = "Combine XYZW"
    nl_module = 'uplogic.nodes.parameters'

    search_tags = [
        ['Combine XYZW', {}],
        ['Vector XYZW', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, 'X')
        self.add_input(NodeSocketLogicFloat, 'Y')
        self.add_input(NodeSocketLogicFloat, 'Z')
        self.add_input(NodeSocketLogicFloat, 'W')
        self.add_output(NodeSocketLogicVectorXYZ, "Vector")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULVectorXYZW"

    def get_output_names(self):
        return ["OUTV"]

    def get_input_names(self):
        return ["input_x", "input_y", "input_z", 'input_w']
