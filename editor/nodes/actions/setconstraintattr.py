from ...sockets.stringsocket import NodeSocketLogicString
from ...sockets.constraintsocket import NodeSocketLogicConstraint
from ...sockets import NodeSocketLogicCondition
from ...sockets.floatsocket import NodeSocketLogicFloat
from ...sockets.objectsocket import NodeSocketLogicObject
from ..node import LogicNodeActionType
from ..node import node_type


@node_type
class LogicNodeSetConstraintAttribute(LogicNodeActionType):
    bl_idname = "LogicNodeSetConstraintAttribute"
    bl_label = "Set Constraint Attribute"
    bl_description = 'Set an attribute of a physics constraint by name'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "SetConstraintAttributeNode"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'object')
        self.add_input(NodeSocketLogicConstraint, "Constraint", 'constraint', {'ref_index': 1})
        self.add_input(NodeSocketLogicString, "Attribute", 'attribute')
        self.add_input(NodeSocketLogicFloat, "Value", 'value')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "object", 'constraint', 'attribute', 'value']
