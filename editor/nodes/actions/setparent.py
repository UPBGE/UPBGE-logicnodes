from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBoolean


_parent_types = [
    ('0', 'Object', '')
]


@node_type
class LogicNodeSetParent(LogicNodeActionType):
    bl_idname = "NLActionSetParentNode"
    bl_label = "Set Parent"
    bl_description = 'Set the parent of an object'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetParent"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Child Object", 'child_object')
        self.add_input(NodeSocketLogicObject, "Parent Object", 'parent_object')
        self.add_input(NodeSocketLogicBoolean, "Compound", 'compound', {'default_value': True, 'enabled': False})
        self.add_input(NodeSocketLogicBoolean, "Ghost", 'ghost', {'default_value': True, 'enabled': False})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "child_object",
            "parent_object",
            "compound",
            "ghost"
        ]
