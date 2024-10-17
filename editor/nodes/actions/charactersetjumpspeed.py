from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicFloatPositive


@node_type
class LogicNodeCharacterSetJumpSpeed(LogicNodeActionType):
    bl_idname = "NLSetCharacterJumpSpeed"
    bl_label = "Set Jump Force"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetCharacterJumpSpeed"
    bl_description = "Set the upwards force used by 'Jump'. Requires 'Character' type physics"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicObject, 'Object', 'game_object')
        self.add_input(NodeSocketLogicFloatPositive, 'Force', 'force')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "game_object", "force"]
