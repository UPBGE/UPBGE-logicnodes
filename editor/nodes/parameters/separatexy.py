from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXY


@node_type
class LogicNodeSeparateXY(LogicNodeParameterType):
    bl_idname = "NLParameterVector2SplitNode"
    bl_label = "Separate XY"
    nl_category = "Values"
    nl_subcat = 'Vectors'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicVectorXY, 'Vector')
        self.add_output(NodeSocketLogicFloat, "X")
        self.add_output(NodeSocketLogicFloat, "Y")

    def get_netlogic_class_name(self):
        return "ULVectorSplitXY"

    def get_output_names(self):
        return ["OUTX", "OUTY"]

    def get_input_names(self):
        return ["input_v"]
