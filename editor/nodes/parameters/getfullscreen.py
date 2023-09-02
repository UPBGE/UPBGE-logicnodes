from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeGetFullscreen(LogicNodeParameterType):
    bl_idname = "NLGetFullscreen"
    bl_label = "Get Fullscreen"
    nl_category = 'Render'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_output(NodeSocketLogicParameter, "Fullscreen")

    def get_netlogic_class_name(self):
        return "ULGetFullscreen"

    def get_output_names(self):
        return ['OUT']
