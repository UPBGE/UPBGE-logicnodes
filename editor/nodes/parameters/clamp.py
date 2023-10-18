from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeClamp(LogicNodeParameterType):
    bl_idname = "NLClampValueNode"
    bl_label = "Clamp"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "Value")
        self.add_input(NodeSocketLogicVectorXY, "", {'enabled': False})
        self.add_input(NodeSocketLogicFloat, "Min")
        self.add_input(NodeSocketLogicFloat, "Max", {'default_value': 1.0})
        self.add_output(NodeSocketLogicFloat, "Value")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULClamp"

    def get_input_names(self):
        return ["value", "range", "min_value", "max_value"]

    def get_output_names(self):
        return ['OUT']
