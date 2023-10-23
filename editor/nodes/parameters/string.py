from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeString(LogicNodeParameterType):
    bl_idname = "NLParameterStringValue"
    bl_label = "String"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULSimpleValue"
    deprecated = True

    def init(self, context):
        self.add_input(NodeSocketLogicString, "")
        self.add_output(NodeSocketLogicString, "String")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["value"]

    def get_output_names(self):
        return ["OUT"]
