from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeRemovePhysicsConstraint(LogicNodeActionType):
    bl_idname = "NLActionRemovePhysicsConstraint"
    bl_label = "Remove Constraint"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULRemovePhysicsConstraint"
    bl_description = 'Remove a named physics constraint from an object'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'object')
        self.add_input(NodeSocketLogicString, "Name", 'name')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "object", "name"]
