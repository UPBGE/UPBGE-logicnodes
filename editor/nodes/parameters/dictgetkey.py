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
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicDictionary, "Dictionary")
        self.add_input(NodeSocketLogicString, "Key", {'default_value': 'key'})
        self.add_input(NodeSocketLogicValueOptional, "Default Value")
        self.add_output(NodeSocketLogicParameter, "Property Value")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULDictValue"

    def get_input_names(self):
        return ["dict", "key", 'default_value']

    def get_output_names(self):
        return ['OUT']
