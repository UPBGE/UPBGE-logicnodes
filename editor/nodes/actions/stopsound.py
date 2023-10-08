from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicPython


@node_type
class LogicNodeStopSound(LogicNodeActionType):
    bl_idname = "NLActionStopSound"
    bl_label = "Stop Sound"
    nl_module = 'actions'
    nl_class = "ULStopSound"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicPython, "Sound")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ["condition", "sound"]
