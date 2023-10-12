from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicInteger


@node_type
class LogicNodeMouseData(LogicNodeParameterType):
    bl_idname = "NLMouseDataParameter"
    bl_label = "Mouse Status"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULMouseData"

    search_tags = [
        ['Mouse Position', {'nl_label': 'Mouse Position', 'disable_out': [1, 4, 5, 6]}],
        ['Mouse Movement', {'nl_label': 'Mouse Movement', 'disable_out': [0, 2, 3, 6]}],
        ['Mouse Wheel', {'nl_label': 'Mouse Wheel', 'disable_out': [0, 1, 2, 3, 4, 5]}],
        ['Mouse Status', {}]
    ]

    def init(self, context):
        self.add_output(NodeSocketLogicVectorXYZ, "Position")
        self.add_output(NodeSocketLogicVectorXYZ, "Movement")
        self.add_output(NodeSocketLogicParameter, "X Position")
        self.add_output(NodeSocketLogicParameter, "Y Position")
        self.add_output(NodeSocketLogicParameter, "X Movement")
        self.add_output(NodeSocketLogicParameter, "Y Movement")
        self.add_output(NodeSocketLogicInteger, "Wheel Difference")
        LogicNodeParameterType.init(self, context)

    def get_output_names(self):
        return ["MXY0", "MDXY0", "MX", "MY", "MDX", "MDY", "MDWHEEL"]
