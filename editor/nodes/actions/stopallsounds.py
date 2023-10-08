from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition


@node_type
class LogicNodeStopAllSounds(LogicNodeActionType):
    bl_idname = "NLActionStopAllSounds"
    bl_label = "Stop All Sounds"
    nl_module = 'actions'
    nl_class = "ULStopAllSounds"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ["condition"]
