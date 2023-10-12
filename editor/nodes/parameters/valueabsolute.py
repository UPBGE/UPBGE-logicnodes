from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeValueAbsolute(LogicNodeParameterType):
    bl_idname = "NLAbsoluteValue"
    bl_label = "Absolute"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "Value")
        self.add_output(NodeSocketLogicFloat, "Value")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULAbsoluteValue"

    def get_input_names(self):
        return ["value"]

    def get_output_names(self):
        return ['OUT']
