from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicTime
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeTimer(LogicNodeConditionType):
    bl_idname = "NLConditionTimeElapsed"
    bl_label = "Timer"
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULTimer"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Set Timer")
        self.add_input(NodeSocketLogicTime, "Seconds")
        self.add_output(NodeSocketLogicCondition, "When Elapsed")
        LogicNodeConditionType.init(self, context)

    def get_input_names(self):
        return ["condition", "delta_time"]
