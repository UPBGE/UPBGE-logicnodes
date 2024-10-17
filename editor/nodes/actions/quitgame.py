from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeQuitGame(LogicNodeActionType):
    bl_idname = "NLActionEndGame"
    bl_label = "Quit Game"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULEndGame"
    bl_description = 'End game runtime'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition"]
