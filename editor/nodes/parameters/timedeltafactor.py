from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeTimeDeltaFactor(LogicNodeParameterType):
    bl_idname = "LogicNodeTimeFactor"
    bl_label = "Delta Factor"
    nl_module = 'parameters'

    def init(self, context):
        self.add_output(NodeSocketLogicFloat, "Factor")
        LogicNodeParameterType.init(self, context)

    def get_output_names(self):
        return ["TIMEFACTOR"]

    nl_class = "ULFPSFactor"
