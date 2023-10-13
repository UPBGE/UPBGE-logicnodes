from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeOnce(LogicNodeConditionType):
    bl_idname = "NLConditionOnceNode"
    bl_label = "Once"
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULOnce"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicBoolean, "Repeat")
        self.add_input(NodeSocketLogicFloatPositive, 'Reset After', {'value': .5}, {'enabled': False})
        self.add_output(NodeSocketLogicCondition, "Out")
        LogicNodeConditionType.init(self, context)

    def get_input_names(self):
        return ["input_condition", 'repeat', 'reset_time']
