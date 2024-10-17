from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicInteger


@node_type
class LogicNodeListRemoveIndex(LogicNodeActionType):
    bl_idname = "NLRemoveListIndex"
    bl_label = "Remove Index"
    bl_description = 'Remove the value from a list at a specific index'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULRemoveListIndex"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicList, 'List', 'items')
        self.add_input(NodeSocketLogicInteger, 'Index', 'idx')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        self.add_output(NodeSocketLogicList, 'List', 'LIST')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", "LIST"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", 'items', 'idx']
