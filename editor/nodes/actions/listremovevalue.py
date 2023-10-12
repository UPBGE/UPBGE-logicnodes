from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicValue


@node_type
class LogicNodeListRemoveValue(LogicNodeActionType):
    bl_idname = "NLRemoveListValue"
    bl_label = "Remove Value"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULRemoveListValue"

    search_tags = [
        ['Remove List Value', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicList, 'List')
        self.add_input(NodeSocketLogicValue, '')
        self.add_output(NodeSocketLogicCondition, 'Done')
        self.add_output(NodeSocketLogicList, 'List')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT", "LIST"]

    def get_input_names(self):
        return ["condition", 'items', 'val']
