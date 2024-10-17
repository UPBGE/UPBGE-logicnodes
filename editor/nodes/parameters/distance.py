from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeDistance(LogicNodeParameterType):
    bl_idname = "NLParameterDistance"
    bl_label = "Distance"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULDistance"
    deprecated = True
    deprecation_message = 'Replaced by "Vector Math" Node.'

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, "A")
        self.add_input(NodeSocketLogicVectorXYZ, "B")
        self.add_output(NodeSocketLogicFloat, "Distance")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["parama", "paramb"]

    def get_output_names(self):
        return ["OUT"]
