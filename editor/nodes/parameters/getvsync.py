from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeGetVsync(LogicNodeParameterType):
    bl_idname = "NLGetVsyncNode"
    bl_label = "Get VSync"
    bl_description = 'State of vertical sync'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetVSync"

    def init(self, context):
        self.add_output(NodeSocketLogicParameter, "Mode", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
