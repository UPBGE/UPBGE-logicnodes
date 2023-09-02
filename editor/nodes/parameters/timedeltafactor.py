from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeTimeDeltaFactor(LogicNodeParameterType):
    bl_idname = "LogicNodeTimeFactor"
    bl_label = "Delta Factor"
    nl_category = 'Time'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_output(NodeSocketLogicFloat, "Factor")

    def get_output_names(self):
        return ["TIMEFACTOR"]

    def get_netlogic_class_name(self):
        return "ULFPSFactor"
