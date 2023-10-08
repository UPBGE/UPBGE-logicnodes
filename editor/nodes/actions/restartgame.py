from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeRestartGame(LogicNodeActionType):
    bl_idname = "NLActionRestartGame"
    bl_label = "Restart Game"
    nl_module = 'actions'
    nl_class = "ULRestartGame"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition"]
