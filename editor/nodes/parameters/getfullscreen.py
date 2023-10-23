from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeGetFullscreen(LogicNodeParameterType):
    bl_idname = "NLGetFullscreen"
    bl_label = "Get Fullscreen"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_output(NodeSocketLogicParameter, "Fullscreen")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULGetFullscreen"

    def get_output_names(self):
        return ['OUT']
