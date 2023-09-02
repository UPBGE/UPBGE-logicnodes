from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeCombineXYZ(LogicNodeParameterType):
    bl_idname = "NLParameterVector3SimpleNode"
    bl_label = "Combine XYZ"
    nl_category = "Values"
    nl_subcat = 'Vectors'
    nl_module = 'parameters'

    search_tags = [
        ['Combine XYZ', {}],
        ['Vector XYZ', {}]
    ]

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicFloat, 'X')
        self.add_input(NodeSocketLogicFloat, 'Y')
        self.add_input(NodeSocketLogicFloat, 'Z')
        self.add_output(NodeSocketLogicVectorXYZ, "Vector")

    def get_netlogic_class_name(self):
        return "ULVectorXYZ"

    def get_output_names(self):
        return ["OUTV"]

    def get_input_names(self):
        return ["input_x", "input_y", "input_z"]
