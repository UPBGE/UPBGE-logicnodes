from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFont


@node_type
class LogicNodeGetFont(LogicNodeParameterType):
    bl_idname = "LogicNodeGetFont"
    bl_label = "Get Font"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetFont"

    def init(self, context):
        self.add_input(NodeSocketLogicFont, "Font")
        self.add_output(NodeSocketLogicFont, 'Font')
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["font"]

    def get_output_names(self):
        return ['OUT']
