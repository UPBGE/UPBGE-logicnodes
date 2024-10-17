from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXY


@node_type
class LogicNodeSeparateXY(LogicNodeParameterType):
    bl_idname = "NLParameterVector2SplitNode"
    bl_label = "Separate XY"
    bl_description = 'Split a 2D vector into its components'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULVectorSplitXY"

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXY, 'Vector', 'input_v')
        self.add_output(NodeSocketLogicFloat, "X", 'OUTX')
        self.add_output(NodeSocketLogicFloat, "Y", 'OUTY')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUTX", "OUTY"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["input_v"]
