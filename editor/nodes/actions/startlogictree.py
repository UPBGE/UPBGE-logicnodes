from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicTree


@node_type
class LogicNodeStartLogicTree(LogicNodeActionType):
    bl_idname = "NLStartLogicNetworkActionNode"
    bl_label = "Start Logic Tree"
    nl_module = 'actions'
    nl_class = "ULStartSubNetwork"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicObject, 'Object')
        self.add_input(NodeSocketLogicTree, 'Tree Name')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "game_object", "logic_network_name"]
