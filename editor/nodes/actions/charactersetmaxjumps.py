from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicIntegerPositive


@node_type
class LogicNodeCharacterSetMaxJumps(LogicNodeActionType):
    bl_idname = "NLSetActionCharacterJump"
    bl_label = "Set Max Jumps"
    bl_description = "Set the maximum number of jumps that can be made before having to touch the ground. Requires 'Character' type physics"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetCharacterMaxJumps"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicIntegerPositive, "Max Jumps", 'max_jumps')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "game_object", 'max_jumps']
