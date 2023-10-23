from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXY


@node_type
class LogicNodeSeparateXY(LogicNodeParameterType):
    bl_idname = "NLParameterVector2SplitNode"
    bl_label = "Separate XY"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXY, 'Vector')
        self.add_output(NodeSocketLogicFloat, "X")
        self.add_output(NodeSocketLogicFloat, "Y")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULVectorSplitXY"

    def get_output_names(self):
        return ["OUTX", "OUTY"]

    def get_input_names(self):
        return ["input_v"]
