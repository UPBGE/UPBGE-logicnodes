from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetPhysics(LogicNodeActionType):
    bl_idname = "NLActionSetPhysicsNode"
    bl_label = "Set Physics"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetPhysics"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicBoolean, "Active")
        self.add_input(NodeSocketLogicBoolean, "Cut Constraints", {'default_value': False})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "game_object", "activate", 'free_const']
