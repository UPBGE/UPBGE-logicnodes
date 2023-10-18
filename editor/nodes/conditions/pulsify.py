from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicTime
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodePulsify(LogicNodeConditionType):
    """Convert a constant True condition into an interval signal"""
    bl_idname = "NLActionTimeFilter"
    bl_label = "Pulsify"
    nl_module = 'uplogic.nodes.conditions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicTime, "Gap", {'default_value': 1.0})
        self.add_output(NodeSocketLogicCondition, "Out")
        LogicNodeConditionType.init(self, context)

    nl_class = "ULPulsify"

    def get_input_names(self):
        return ["condition", "delay"]
