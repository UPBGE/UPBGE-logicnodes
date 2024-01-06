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

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicVectorXYZVelocity, "Gravity", None, {'default_value': (0., 0., -9.8)})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "game_object", 'gravity']
