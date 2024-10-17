from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicTime
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeTimeBarrier(LogicNodeConditionType):
    """If the condition stays true for N seconds, do something, then stay true"""
    bl_idname = 'NLActionTimeBarrier'
    bl_label = 'Barrier'
    bl_description = 'Only relay a positive condition if it has been "True" for a given amount of time'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = 'ULBarrier'

    search_tags = [
        ['Time Barrier', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicTime, 'Time', 'time')
        self.add_output(NodeSocketLogicCondition, 'Out', 'OUT')
        LogicNodeConditionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['condition', 'time']
