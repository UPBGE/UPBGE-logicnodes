from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicTree


@node_type
class LogicNodeStartLogicTree(LogicNodeActionType):
    bl_idname = "NLStartLogicNetworkActionNode"
    bl_label = "Start Logic Tree"
    bl_description = 'Start a logic tree on another object'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULStartSubNetwork"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicObject, 'Object', 'game_object')
        self.add_input(NodeSocketLogicTree, 'Tree Name', 'logic_network_name')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "game_object", "logic_network_name"]
