from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetRigidBody(LogicNodeActionType):
    bl_idname = "NLSetRigidBody"
    bl_label = "Set Rigid Body"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetRigidBody"
    bl_description = 'Set the rigid body state of an object'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicBoolean, "Enabled", 'activate', {'default_value': True})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "game_object", "activate"]
