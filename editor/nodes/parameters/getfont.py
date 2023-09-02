from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFont


@node_type
class LogicNodeGetFont(LogicNodeParameterType):
    bl_idname = "LogicNodeGetFont"
    bl_label = "Get Font"
    bl_icon = 'FILE_FONT'
    nl_category = "File"
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicFont, "Font")
        self.add_output(NodeSocketLogicFont, 'Font')

    def get_netlogic_class_name(self):
        return "ULGetFont"

    def get_input_names(self):
        return ["font"]

    def get_output_names(self):
        return ['OUT']
