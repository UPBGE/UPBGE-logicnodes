from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFont


@node_type
class LogicNodeGetFont(LogicNodeParameterType):
    bl_idname = "LogicNodeGetFont"
    bl_label = "Get Font"
    bl_description = 'Font(ID)'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetFont"

    def init(self, context):
        self.add_input(NodeSocketLogicFont, "Font", 'font')
        self.add_output(NodeSocketLogicFont, 'Font', 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["font"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
