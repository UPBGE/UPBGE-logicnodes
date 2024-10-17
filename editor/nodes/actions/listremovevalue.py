from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicValue


@node_type
class LogicNodeListRemoveValue(LogicNodeActionType):
    bl_idname = "NLRemoveListValue"
    bl_label = "Remove Value"
    bl_description = 'Remove a value from a list'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULRemoveListValue"

    search_tags = [
        ['Remove List Value', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicList, 'List', 'items')
        self.add_input(NodeSocketLogicValue, '', 'val')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        self.add_output(NodeSocketLogicList, 'List', 'LIST')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", "LIST"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", 'items', 'val']
