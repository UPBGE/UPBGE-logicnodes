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
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULExecuteSubNetwork"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", {'default_value': True, 'show_prop': True})
        self.add_input(NodeSocketLogicObject, "Target Object")
        self.add_input(NodeSocketLogicTree, "Tree Name")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "target_object", "tree_name"]
