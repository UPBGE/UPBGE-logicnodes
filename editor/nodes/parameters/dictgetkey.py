from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicDictionary
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicValueOptional
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeDictGetKey(LogicNodeParameterType):
    bl_idname = "NLGetDictKeyNode"
    bl_label = 'Get Dictionary Key'
    bl_description = 'Value by key of a dictionary'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULDictValue"

    def init(self, context):
        self.add_input(NodeSocketLogicDictionary, "Dictionary", 'dict')
        self.add_input(NodeSocketLogicString, "Key", 'key', {'default_value': 'key'})
        self.add_input(NodeSocketLogicValueOptional, "Default Value", 'default_value')
        self.add_output(NodeSocketLogicParameter, "Property Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["dict", "key", 'default_value']

    def get_output_names(self):
        return ['OUT']
