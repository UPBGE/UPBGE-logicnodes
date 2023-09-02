from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeGetTimescale(LogicNodeParameterType):
    bl_idname = "NLParameterGetTimeScale"
    bl_label = "Get Timescale"
    nl_category = "Scene"
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_output(NodeSocketLogicParameter, 'Timescale')

    def get_netlogic_class_name(self):
        return "ULGetTimeScale"

    def get_output_names(self):
        return ['OUT']
