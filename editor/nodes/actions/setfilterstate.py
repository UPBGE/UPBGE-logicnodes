from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetFilterState(LogicNodeActionType):
    bl_idname = "NLSetFilterState"
    bl_label = "Set Filter State"
    bl_description = 'Set the activity status of a screen filter'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetFilterState"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Pass Index', 'pass_idx')
        self.add_input(NodeSocketLogicBoolean, 'Active', 'state')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['condition', 'pass_idx', 'state']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
