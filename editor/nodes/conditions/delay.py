from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicTime
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeDelay(LogicNodeConditionType):
    bl_idname = 'NLActionTimeDelay'
    bl_label = 'Delay'
    bl_icon = 'PREVIEW_RANGE'
    nl_category = 'Time'
    nl_module = 'conditions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicTime, 'Delay')
        self.add_output(NodeSocketLogicCondition, 'Out')
        LogicNodeConditionType.init(self, context)

    nl_class = 'ULTimeDelay'

    def get_input_names(self):
        return ['condition', 'delay']
