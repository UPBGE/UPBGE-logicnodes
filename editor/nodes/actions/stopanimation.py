from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicIntegerPositive


@node_type
class LogicNodeStopAnimation(LogicNodeActionType):
    bl_idname = "NLActionStopAnimation"
    bl_label = "Stop Animation"
    nl_category = "Animation"
    nl_module = 'actions'
    nl_class = "ULStopAction"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicIntegerPositive, "Animation Layer")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "game_object", "action_layer"]
