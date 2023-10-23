from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeSeparateXYZ(LogicNodeParameterType):
    bl_idname = "NLParameterVector3SplitNode"
    bl_label = "Separate XYZ"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, 'Vector')
        self.add_output(NodeSocketLogicFloat, "X")
        self.add_output(NodeSocketLogicFloat, "Y")
        self.add_output(NodeSocketLogicFloat, "Z")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULVectorSplitXYZ"

    def get_output_names(self):
        return ["OUTX", "OUTY", 'OUTZ']

    def get_input_names(self):
        return ["input_v"]
