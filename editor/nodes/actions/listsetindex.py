from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicValue


@node_type
class LogicNodeListSetIndex(LogicNodeActionType):
    bl_idname = "NLSetListIndex"
    bl_label = "Set List Index"
    bl_description = 'Set an index of a list to a specific value'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetListIndex"

    search_tags = [
        ['Set List Index', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicList, 'List', 'items')
        self.add_input(NodeSocketLogicInteger, 'Index', 'index')
        self.add_input(NodeSocketLogicValue, '', 'val')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        self.add_output(NodeSocketLogicList, 'List', 'LIST')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", "LIST"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", 'items', 'index', 'val']
