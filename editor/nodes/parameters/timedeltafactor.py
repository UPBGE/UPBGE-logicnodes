from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeTimeDeltaFactor(LogicNodeParameterType):
    bl_idname = "LogicNodeTimeFactor"
    bl_label = "Delta Factor"
    bl_description = 'Time per frame compared to 60 fps'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULFPSFactor"

    def init(self, context):
        self.add_output(NodeSocketLogicFloat, "Factor", 'TIMEFACTOR')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["TIMEFACTOR"]
