from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeBoolean(LogicNodeParameterType):
    bl_idname = "NLParameterBooleanValue"
    bl_label = "Boolean"
    bl_icon = 'CHECKBOX_HLT'
    nl_category = "Values"
    nl_subcat = 'Simple'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicBoolean, "Bool")
        self.add_output(NodeSocketLogicBoolean, "Bool")

    def get_netlogic_class_name(self):
        return "ULSimpleValue"

    def get_input_names(self):
        return ["value"]

    def get_output_names(self):
        return ["OUT"]
