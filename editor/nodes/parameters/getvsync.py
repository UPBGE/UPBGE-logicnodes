from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeGetVsync(LogicNodeParameterType):
    bl_idname = "NLGetVsyncNode"
    bl_label = "Get VSync"
    nl_module = 'parameters'

    def init(self, context):
        self.add_output(NodeSocketLogicParameter, "Mode")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULGetVSync"

    def get_output_names(self):
        return ['OUT']
