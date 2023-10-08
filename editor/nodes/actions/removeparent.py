from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeRemoveParent(LogicNodeActionType):
    bl_idname = "NLActionRemoveParentNode"
    bl_label = "Remove Parent"
    nl_module = 'actions'
    nl_class = "ULRemoveParent"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Child Object")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "child_object"]
