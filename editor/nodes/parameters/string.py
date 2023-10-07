from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeString(LogicNodeParameterType):
    bl_idname = "NLParameterStringValue"
    bl_icon = 'FONT_DATA'
    bl_label = "String"
    nl_module = 'parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicString, "")
        self.add_output(NodeSocketLogicString, "String")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULSimpleValue"

    def get_input_names(self):
        return ["value"]

    def get_output_names(self):
        return ["OUT"]
