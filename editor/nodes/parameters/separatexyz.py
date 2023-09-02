from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeSeparateXYZ(LogicNodeParameterType):
    bl_idname = "NLParameterVector3SplitNode"
    bl_label = "Separate XYZ"
    nl_category = "Values"
    nl_subcat = 'Vectors'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicVectorXYZ, 'Vector')
        self.add_output(NodeSocketLogicFloat, "X")
        self.add_output(NodeSocketLogicFloat, "Y")
        self.add_output(NodeSocketLogicFloat, "Z")

    def get_netlogic_class_name(self):
        return "ULVectorSplitXYZ"

    def get_output_names(self):
        return ["OUTX", "OUTY", 'OUTZ']

    def get_input_names(self):
        return ["input_v"]
