from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXY


@node_type
class LogicNodeCombineXY(LogicNodeParameterType):
    bl_idname = "NLParameterVector2SimpleNode"
    bl_label = "Combine XY"
    nl_category = "Values"
    nl_subcat = 'Vectors'
    nl_module = 'parameters'

    search_tags = [
        ['Combine XY', {}],
        ['Vector XY', {}]
    ]

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicFloat, 'X')
        self.add_input(NodeSocketLogicFloat, 'Y')
        self.add_output(NodeSocketLogicVectorXY, "Vector")

    def get_netlogic_class_name(self):
        return "ULVectorXY"

    def get_output_names(self):
        return ["OUTV"]

    def get_input_names(self):
        return ["input_x", "input_y"]
