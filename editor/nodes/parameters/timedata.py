from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeTimeData(LogicNodeParameterType):
    bl_idname = "NLParameterTimeNode"
    bl_label = "Time Data"
    nl_category = 'Time'
    nl_module = 'parameters'

    search_tags = [
        ['Time', {'disable_out': [1, 2]}],
        ['Time Delta', {'disable_out': [0, 2]}],
        ['Frametime', {'disable_out': [0, 2]}],
        ['FPS', {'disable_out': [0, 1]}],
        ['Time Data', {}]
    ]

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_output(NodeSocketLogicFloat, "Time")
        self.add_output(NodeSocketLogicFloat, "Delta (Frametime)")
        self.add_output(NodeSocketLogicFloat, "FPS")

    def get_output_names(self):
        return ["TIMELINE", "TIME_PER_FRAME", "FPS"]

    def get_netlogic_class_name(self):
        return "ULTimeData"
