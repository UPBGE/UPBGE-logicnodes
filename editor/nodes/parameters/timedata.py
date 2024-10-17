from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeTimeData(LogicNodeParameterType):
    bl_idname = "NLParameterTimeNode"
    bl_label = "Time Data"
    bl_description = 'Elapsed time, FPS and time per frame'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULTimeData"

    search_tags = [
        ['Time', {'disable_out': [1, 2]}],
        ['Time Delta', {'disable_out': [0, 2]}],
        ['Frametime', {'disable_out': [0, 2]}],
        ['FPS', {'disable_out': [0, 1]}],
        ['Time Data', {}]
    ]

    def init(self, context):
        self.add_output(NodeSocketLogicFloat, "Time", 'TIMELINE')
        self.add_output(NodeSocketLogicFloat, "Delta (Frametime)", 'TIME_PER_FRAME')
        self.add_output(NodeSocketLogicFloat, "FPS", 'FPS')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["TIMELINE", "TIME_PER_FRAME", "FPS"]
