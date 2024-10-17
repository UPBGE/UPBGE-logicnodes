from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicDictionary
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeDictionaryRemoveKey(LogicNodeActionType):
    bl_idname = "NLSetDictDelKey"
    bl_label = "Remove Dictionary Key"
    bl_description = 'Remove a key and its value from a dictionary'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULPopDictKey"

    search_tags = [
        ['Remove Dictionary Key', {}],
        ['Pop Dictionary Key', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicDictionary, 'Dictionary', 'dict')
        self.add_input(NodeSocketLogicString, 'Key', 'key')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        self.add_output(NodeSocketLogicDictionary, 'Dictionary', 'DICT')
        self.add_output(NodeSocketLogicParameter, 'Value', 'VALUE')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", "DICT", 'VALUE']

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", 'dict', 'key']
