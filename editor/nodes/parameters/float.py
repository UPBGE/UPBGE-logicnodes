from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeFloat(LogicNodeParameterType):
    bl_idname = "NLParameterFloatValue"
    bl_label = "Float"
    nl_class = "ULSimpleValue"
    nl_module = 'uplogic.nodes.parameters'
    deprecated = True

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "", 'value')
        self.add_output(NodeSocketLogicFloat, "Float", 'OUT')
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["value"]

    def get_output_names(self):
        return ["OUT"]
