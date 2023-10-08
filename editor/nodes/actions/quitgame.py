from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeQuitGame(LogicNodeActionType):
    bl_idname = "NLActionEndGame"
    bl_label = "Quit Game"
    nl_module = 'actions'
    nl_class = "ULEndGame"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ["condition"]
