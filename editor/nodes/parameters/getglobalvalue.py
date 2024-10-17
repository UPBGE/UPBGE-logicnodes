from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicGlobalCategory
from ...sockets import NodeSocketLogicGlobalProperty
from ...sockets import NodeSocketLogicValueOptional
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeGetGlobalValue(LogicNodeParameterType):
    bl_idname = "NLParameterGetGlobalValue"
    bl_label = "Get Global Property"
    bl_description = 'Retrieve a globally stored value'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetGlobalValue"

    def init(self, context):
        self.add_input(NodeSocketLogicGlobalCategory, "Category", 'data_id')
        self.add_input(NodeSocketLogicGlobalProperty, "Property", 'key')
        self.add_input(NodeSocketLogicValueOptional, "Default Value", 'default')
        self.add_output(NodeSocketLogicParameter, "Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["data_id", "key", 'default']

    def get_output_names(self):
        return ["OUT"]
