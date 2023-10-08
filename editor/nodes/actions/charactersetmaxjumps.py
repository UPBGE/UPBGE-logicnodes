from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicIntegerPositive


@node_type
class LogicNodeCharacterSetMaxJumps(LogicNodeActionType):
    bl_idname = "NLSetActionCharacterJump"
    bl_label = "Set Max Jumps"
    nl_module = 'actions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicIntegerPositive, "Max Jumps")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    nl_class = "ULSetCharacterMaxJumps"

    def get_input_names(self):
        return ["condition", "game_object", 'max_jumps']
