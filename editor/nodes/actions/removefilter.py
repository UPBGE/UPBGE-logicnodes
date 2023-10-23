from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicIntegerPositiveCent


@node_type
class LogicNodeRemoveFilter(LogicNodeActionType):
    bl_idname = "NLRemoveFilter"
    bl_label = "Remove Filter"
    nl_module = 'uplogic.nodes.actions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Pass Index')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ['condition', 'pass_idx']

    def get_output_names(self):
        return ["OUT"]

    nl_class = "ULRemoveFilter"
