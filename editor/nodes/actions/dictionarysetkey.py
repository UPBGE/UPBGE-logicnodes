from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicDictionary
from ...sockets import NodeSocketLogicValue


@node_type
class LogicNodeDictionarySetKey(LogicNodeActionType):
    bl_idname = "NLSetDictKeyValue"
    bl_label = "Set Key"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetDictKey"

    search_tags = [
        ['Set Dictionary Key', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicDictionary, 'Dictionary')
        self.add_input(NodeSocketLogicString, 'Key')
        self.add_input(NodeSocketLogicValue, '')
        self.add_output(NodeSocketLogicCondition, 'Done')
        self.add_output(NodeSocketLogicDictionary, 'Dictionary')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT", "DICT"]

    def get_input_names(self):
        return ["condition", 'dict', 'key', 'val']
