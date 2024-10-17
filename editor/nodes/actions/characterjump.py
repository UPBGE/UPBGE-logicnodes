from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeCharacterJump(LogicNodeActionType):
    bl_idname = "NLActionCharacterJump"
    bl_label = "Jump"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULCharacterJump"
    bl_description = "Apply upwards force if on ground. Requires 'Character' type physics"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicObject, 'Object', 'game_object')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "game_object"]
