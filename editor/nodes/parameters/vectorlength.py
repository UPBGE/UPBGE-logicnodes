from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeVectorLength(LogicNodeParameterType):
    bl_idname = "NLVectorLength"
    bl_label = "Vector Length"
    nl_module = 'parameters'
    deprecated = True
    deprecation_message = 'Replaced by "Random Value" Node.'

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, "Vector")
        self.add_output(NodeSocketLogicFloat, 'Length')
        LogicNodeParameterType.init(self, context)

    nl_class = "ULVectorLength"

    def get_output_names(self):
        return ["OUTV"]

    def get_input_names(self):
        return ["input_v"]
