from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeFloat(LogicNodeParameterType):
    bl_idname = "NLParameterFloatValue"
    bl_label = "Float"
    nl_module = 'uplogic.nodes.parameters'
    deprecated = True

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "")
        self.add_output(NodeSocketLogicFloat, "Float")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULSimpleValue"

    def get_input_names(self):
        return ["value"]

    def get_output_names(self):
        return ["OUT"]
