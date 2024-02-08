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
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULPopDictKey"

    search_tags = [
        ['Remove Dictionary Key', {}],
        ['Pop Dictionary Key', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicDictionary, 'Dictionary')
        self.add_input(NodeSocketLogicString, 'Key')
        self.add_output(NodeSocketLogicCondition, 'Done')
        self.add_output(NodeSocketLogicDictionary, 'Dictionary')
        self.add_output(NodeSocketLogicParameter, 'Value')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT", "DICT", 'VALUE']

    def get_input_names(self):
        return ["condition", 'dict', 'key']
