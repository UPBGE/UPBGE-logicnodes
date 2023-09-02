from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicDictionary
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicValueOptional
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeGetDictKey(LogicNodeParameterType):
    bl_idname = "NLGetDictKeyNode"
    bl_label = 'Get Key'
    nl_category = "Data"
    nl_subcat = 'Dictionary'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicDictionary, "Dictionary")
        self.add_input(NodeSocketLogicString, "Key", {'value': 'key'})
        self.add_input(NodeSocketLogicValueOptional, "Default Value")
        self.add_output(NodeSocketLogicParameter, "Property Value")

    def get_netlogic_class_name(self):
        return "ULDictValue"

    def get_input_names(self):
        return ["dict", "key", 'default_value']

    def get_output_names(self):
        return ['OUT']
