from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicCondition
from ....utilities import OUTCELL


@node_type
class LogicNodeGamepadActive(LogicNodeConditionType):
    bl_idname = "NLGamepadActive"
    bl_label = "Gamepad Active"
    nl_module = 'uplogic.nodes.conditions'

    def init(self, context):
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Index')
        self.add_output(NodeSocketLogicCondition, 'Active')
        LogicNodeConditionType.init(self, context)

    nl_class = "ULGamepadActive"

    def get_input_names(self):
        return ["index"]

    def get_output_names(self):
        return [OUTCELL]
