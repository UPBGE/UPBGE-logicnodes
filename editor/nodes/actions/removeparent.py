from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeRemoveParent(LogicNodeActionType):
    bl_idname = "NLActionRemoveParentNode"
    bl_label = "Remove Parent"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULRemoveParent"
    bl_description = 'Decouple a child from its parent'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Child Object", 'child_object')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        self.add_output(NodeSocketLogicObject, "Parent Object", 'PARENT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", 'PARENT']

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "child_object"]
