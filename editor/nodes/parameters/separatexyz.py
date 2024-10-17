from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeSeparateXYZ(LogicNodeParameterType):
    bl_idname = "NLParameterVector3SplitNode"
    bl_label = "Separate XYZ"
    bl_description = 'Split a 3D vector into its components'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULVectorSplitXYZ"

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, 'Vector', 'input_v')
        self.add_output(NodeSocketLogicFloat, "X", 'OUTX')
        self.add_output(NodeSocketLogicFloat, "Y", 'OUTY')
        self.add_output(NodeSocketLogicFloat, "Z", 'OUTZ')
        LogicNodeParameterType.init(self, context)

    def get_output_names(self):
        return ["OUTX", "OUTY", 'OUTZ']

    def get_input_names(self):
        return ["input_v"]
