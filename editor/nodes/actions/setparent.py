from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetParent(LogicNodeActionType):
    bl_idname = "NLActionSetParentNode"
    bl_label = "Set Parent"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetParent"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Child Object")
        self.add_input(NodeSocketLogicObject, "Parent Object")
        self.add_input(NodeSocketLogicBoolean, "Compound", None, {'default_value': True, 'enabled': False})
        self.add_input(NodeSocketLogicBoolean, "Ghost", None, {'default_value': True, 'enabled': False})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return [
            "condition",
            "child_object",
            "parent_object",
            "compound",
            "ghost"
        ]
