from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetDynamics(LogicNodeActionType):
    bl_idname = "NLActionSetDynamicsNode"
    bl_label = "Set Dynamics"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetDynamics"
    bl_description = 'Set the dynamics activity state of an object'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicBoolean, "Active", 'activate')
        self.add_input(NodeSocketLogicBoolean, "Ghost", 'ghost', {'default_value': False})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "game_object", "activate", 'ghost']
