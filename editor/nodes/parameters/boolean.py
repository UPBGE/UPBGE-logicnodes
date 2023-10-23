from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeBoolean(LogicNodeParameterType):
    bl_idname = "NLParameterBooleanValue"
    bl_label = "Boolean"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULSimpleValue"
    deprecated = True

    def init(self, context):
        self.add_input(NodeSocketLogicBoolean, "Bool")
        self.add_output(NodeSocketLogicBoolean, "Bool")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["value"]

    def get_output_names(self):
        return ["OUT"]
