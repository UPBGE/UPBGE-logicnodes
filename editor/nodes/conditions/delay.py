from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicTime
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeDelay(LogicNodeConditionType):
    bl_idname = 'NLActionTimeDelay'
    bl_label = 'Delay'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = 'ULTimeDelay'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicTime, 'Delay')
        self.add_output(NodeSocketLogicCondition, 'Out')
        LogicNodeConditionType.init(self, context)

    def get_input_names(self):
        return ['condition', 'delay']
