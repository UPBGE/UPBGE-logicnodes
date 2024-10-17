from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicDictionary
from ...sockets import NodeSocketLogicValue


@node_type
class LogicNodeDictionarySetKey(LogicNodeActionType):
    bl_idname = "NLSetDictKeyValue"
    bl_label = "Set Dictionary Key"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetDictKey"
    bl_description = 'Define a value for a key in a dictionary'

    search_tags = [
        ['Set Dictionary Key', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicDictionary, 'Dictionary', 'dict')
        self.add_input(NodeSocketLogicString, 'Key', 'key')
        self.add_input(NodeSocketLogicValue, '', 'val')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        self.add_output(NodeSocketLogicDictionary, 'Dictionary', 'DICT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", "DICT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", 'dict', 'key', 'val']
