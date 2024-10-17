from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicTree


@node_type
class LogicNodeRunLogicTree(LogicNodeActionType):
    bl_idname = "NLActionExecuteNetwork"
    bl_label = "Run Logic Tree"
    bl_description = 'Execute another logic tree on an object'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULExecuteSubNetwork"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition', {'default_value': True, 'show_prop': True})
        self.add_input(NodeSocketLogicObject, "Target Object", 'target_object')
        self.add_input(NodeSocketLogicTree, "Tree Name", 'tree_name')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "target_object", "tree_name"]
