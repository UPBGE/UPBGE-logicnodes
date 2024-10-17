from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXY


@node_type
class LogicNodeCombineXY(LogicNodeParameterType):
    bl_idname = "NLParameterVector2SimpleNode"
    bl_label = "Combine XY"
    bl_description = 'Two-dimensional vector'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULVectorXY"

    search_tags = [
        ['Combine XY', {}],
        ['Vector XY', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, 'X', 'input_x')
        self.add_input(NodeSocketLogicFloat, 'Y', 'input_y')
        self.add_output(NodeSocketLogicVectorXY, "Vector", 'OUTV')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUTV"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["input_x", "input_y"]
