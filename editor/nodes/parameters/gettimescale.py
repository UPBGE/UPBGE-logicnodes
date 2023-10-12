from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeGetTimescale(LogicNodeParameterType):
    bl_idname = "NLParameterGetTimeScale"
    bl_label = "Get Timescale"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_output(NodeSocketLogicParameter, 'Timescale')
        LogicNodeParameterType.init(self, context)

    nl_class = "ULGetTimeScale"

    def get_output_names(self):
        return ['OUT']
