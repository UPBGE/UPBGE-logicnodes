from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicFloatPositive


@node_type
class LogicNodeCharacterSetJumpSpeed(LogicNodeActionType):
    bl_idname = "NLSetCharacterJumpSpeed"
    bl_label = "Set Jump Force"
    nl_module = 'actions'
    nl_class = "ULSetCharacterJumpSpeed"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicObject, 'Object')
        self.add_input(NodeSocketLogicFloatPositive, 'Force')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "game_object", "force"]
