from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicIntegerPositiveCent


@node_type
class LogicNodeRemoveFilter(LogicNodeActionType):
    bl_idname = "NLRemoveFilter"
    bl_label = "Remove Filter"
    bl_description = 'Remove a screen effect from an index'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULRemoveFilter"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Pass Index', 'pass_idx')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['condition', 'pass_idx']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
