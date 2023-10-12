from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicInteger


@node_type
class LogicNodeRandomInteger(LogicNodeParameterType):
    bl_idname = "NLActionRandomInteger"
    bl_label = "Random Integer"
    nl_module = 'uplogic.nodes.parameters'
    deprecated = True
    deprecation_message = 'Replaced by "Random Value" Node.'

    def init(self, context):
        self.add_input(NodeSocketLogicInteger, "Min")
        self.add_input(NodeSocketLogicInteger, "Max")
        self.add_output(NodeSocketLogicInteger, "Value")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["min_value", "max_value"]

    nl_class = "ULRandomInt"

    def get_output_names(self):
        return ["OUT_A"]
