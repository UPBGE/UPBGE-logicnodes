from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetDynamics(LogicNodeActionType):
    bl_idname = "NLActionSetDynamicsNode"
    bl_label = "Set Dynamics"
    nl_module = 'actions'
    nl_class = "ULSetDynamics"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicBoolean, "Active")
        self.add_input(NodeSocketLogicBoolean, "Ghost", {'value': False})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "game_object", "activate", 'ghost']
