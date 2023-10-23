from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetFilterState(LogicNodeActionType):
    bl_idname = "NLSetFilterState"
    bl_label = "Set Filter State"
    nl_module = 'uplogic.nodes.actions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Pass Index')
        self.add_input(NodeSocketLogicBoolean, 'Active')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ['condition', 'pass_idx', 'state']

    def get_output_names(self):
        return ["OUT"]

    nl_class = "ULSetFilterState"
