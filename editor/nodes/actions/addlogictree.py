from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicTree
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeAddLogicTree(LogicNodeActionType):
    bl_idname = "NLActionInstallSubNetwork"
    bl_label = "Add Logic Tree to Object"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULInstallSubNetwork"
    bl_description = 'Apply a new logic tree to an object'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Target Object", 'target_object')
        self.add_input(NodeSocketLogicTree, "Tree Name", 'tree_name')
        self.add_input(NodeSocketLogicBoolean, "Initialize", 'initial_status')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "target_object", "tree_name", "initial_status"]
