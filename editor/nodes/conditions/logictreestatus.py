from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicTree
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeLogicTreeStatus(LogicNodeConditionType):
    bl_idname = "NLConditionLogitNetworkStatusNode"
    bl_label = "Logic Tree Status"
    nl_module = 'conditions'

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicTree, "Tree Name")
        self.add_output(NodeSocketLogicCondition, "Running")
        self.add_output(NodeSocketLogicCondition, "Stopped")
        LogicNodeConditionType.init(self, context)

    nl_class = "ULLogicTreeStatus"

    def get_input_names(self):
        return ["game_object", "tree_name"]

    def get_output_names(self):
        return ["IFRUNNING", "IFSTOPPED"]
