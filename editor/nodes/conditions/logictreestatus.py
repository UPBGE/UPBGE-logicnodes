from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicTree
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeLogicTreeStatus(LogicNodeConditionType):
    bl_idname = "NLConditionLogitNetworkStatusNode"
    bl_label = "Logic Tree Status"
    bl_description = 'Execution status of a logic tree applied to an object'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULLogicTreeStatus"

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicTree, "Tree Name", 'tree_name')
        self.add_output(NodeSocketLogicCondition, "Running", 'IFRUNNING')
        self.add_output(NodeSocketLogicCondition, "Stopped", 'IFSTOPPED')
        LogicNodeConditionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["game_object", "tree_name"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["IFRUNNING", "IFSTOPPED"]
