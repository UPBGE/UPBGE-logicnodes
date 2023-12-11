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
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicGlobalCategory, "Category")
        self.add_input(NodeSocketLogicGlobalProperty, "Property")
        self.add_input(NodeSocketLogicValueOptional, "Default Value")
        self.add_output(NodeSocketLogicParameter, "Value")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["data_id", "key", 'default']

    nl_class = "ULGetGlobalValue"

    def get_output_names(self):
        return ["OUT"]
