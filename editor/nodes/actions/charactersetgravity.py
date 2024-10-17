from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVectorXYZVelocity


@node_type
class LogicNodeCharacterSetGravity(LogicNodeActionType):
    bl_idname = "NLActionSetCharacterGravity"
    bl_label = "Set Gravity"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetCharacterGravity"
    bl_description = "Set the general downwards force. Requires 'Character' type physics"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicVectorXYZVelocity, "Gravity", 'gravity', {'default_value': (0., 0., -9.8)})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "game_object", 'gravity']
