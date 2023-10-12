from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicInteger


@node_type
class LogicNodeListRemoveIndex(LogicNodeActionType):
    bl_idname = "NLRemoveListIndex"
    bl_label = "Remove Index"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULRemoveListIndex"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicList, 'List')
        self.add_input(NodeSocketLogicInteger, 'Index')
        self.add_output(NodeSocketLogicCondition, 'Done')
        self.add_output(NodeSocketLogicList, 'List')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT", "LIST"]

    def get_input_names(self):
        return ["condition", 'items', 'idx']
