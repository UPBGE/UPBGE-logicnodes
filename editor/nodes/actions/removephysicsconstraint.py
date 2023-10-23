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

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicString, "Name")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "object", "name"]
