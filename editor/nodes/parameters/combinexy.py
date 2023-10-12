from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXY


@node_type
class LogicNodeCombineXY(LogicNodeParameterType):
    bl_idname = "NLParameterVector2SimpleNode"
    bl_label = "Combine XY"
    nl_module = 'uplogic.nodes.parameters'

    search_tags = [
        ['Combine XY', {}],
        ['Vector XY', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, 'X')
        self.add_input(NodeSocketLogicFloat, 'Y')
        self.add_output(NodeSocketLogicVectorXY, "Vector")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULVectorXY"

    def get_output_names(self):
        return ["OUTV"]

    def get_input_names(self):
        return ["input_x", "input_y"]
