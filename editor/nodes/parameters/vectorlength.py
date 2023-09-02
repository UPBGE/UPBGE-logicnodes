from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeVectorLength(LogicNodeParameterType):
    bl_idname = "NLVectorLength"
    bl_label = "Vector Length"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    nl_module = 'parameters'
    deprecated = True

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicVectorXYZ, "Vector")
        self.add_output(NodeSocketLogicFloat, 'Length')

    def get_netlogic_class_name(self):
        return "ULVectorLength"

    def get_output_names(self):
        return ["OUTV"]

    def get_input_names(self):
        return ["input_v"]
