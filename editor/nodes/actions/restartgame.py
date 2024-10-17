from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeRestartGame(LogicNodeActionType):
    bl_idname = "NLActionRestartGame"
    bl_label = "Restart Game"
    bl_description = 'Start the current file from its last saved state'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULRestartGame"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition"]
