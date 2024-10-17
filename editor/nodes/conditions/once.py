from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeOnce(LogicNodeConditionType):
    bl_idname = "NLConditionOnceNode"
    bl_label = "Once"
    bl_description = 'Only relay the first of a consecutive "True" condition'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULOnce"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'input_condition')
        self.add_input(NodeSocketLogicBoolean, "Repeat", 'repeat')
        self.add_input(NodeSocketLogicFloatPositive, 'Reset After', 'reset_time', {'default_value': .5, 'enabled': False})
        self.add_output(NodeSocketLogicCondition, "Out", 'OUT')
        LogicNodeConditionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["input_condition", 'repeat', 'reset_time']
