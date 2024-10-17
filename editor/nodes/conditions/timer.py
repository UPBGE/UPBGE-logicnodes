from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicTime
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeTimer(LogicNodeConditionType):
    bl_idname = "NLConditionTimeElapsed"
    bl_label = "Timer"
    bl_description = 'Set a timer'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULTimer"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Set Timer", 'condition')
        self.add_input(NodeSocketLogicTime, "Seconds", 'delta_time')
        self.add_output(NodeSocketLogicCondition, "When Elapsed", 'OUT')
        LogicNodeConditionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "delta_time"]
