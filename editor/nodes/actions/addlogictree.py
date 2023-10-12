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

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Target Object")
        self.add_input(NodeSocketLogicTree, "Tree Name")
        self.add_input(NodeSocketLogicBoolean, "Initialize")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "target_object", "tree_name", "initial_status"]
