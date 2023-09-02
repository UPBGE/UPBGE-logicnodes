from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeVectorAbsolute(LogicNodeParameterType):
    bl_idname = "NLParameterAbsVector3Node"
    bl_label = "Absolute Vector"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicVectorXYZ, 'Vector')
        self.add_output(NodeSocketLogicVectorXYZ, "Vector")

    def get_netlogic_class_name(self):
        return "ULVectorAbsolute"

    def get_output_names(self):
        return ["OUTV"]

    def get_input_names(self):
        return ["input_v"]