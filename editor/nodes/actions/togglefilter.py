from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicIntegerPositiveCent


@node_type
class LogicNodeToggleFilter(LogicNodeActionType):
    bl_idname = "NLToggleFilter"
    bl_label = "Toggle Filter"
    nl_module = 'actions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Pass Index')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ['condition', 'pass_idx']

    def get_output_names(self):
        return ["OUT"]

    nl_class = "ULToggleFilter"
