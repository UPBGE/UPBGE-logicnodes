from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicValue


@node_type
class LogicNodeListAppend(LogicNodeActionType):
    bl_idname = "NLAppendListItem"
    bl_label = "Append"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULAppendListItem"

    search_tags = [
        ['List Append', {}]
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
