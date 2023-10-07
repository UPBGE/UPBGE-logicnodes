from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicTime
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeTimeBarrier(LogicNodeConditionType):
    """If the condition stays true for N seconds, do something, then stay true"""
    bl_idname = 'NLActionTimeBarrier'
    bl_label = 'Barrier'
    nl_module = 'conditions'

    search_tags = [
        ['Time Barrier', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicTime, 'Time')
        self.add_output(NodeSocketLogicCondition, 'Out')
        LogicNodeConditionType.init(self, context)

    nl_class = 'ULBarrier'

    def get_input_names(self):
        return ['condition', 'time']
