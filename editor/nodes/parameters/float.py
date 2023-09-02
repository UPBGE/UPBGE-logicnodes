from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeFloat(LogicNodeParameterType):
    bl_idname = "NLParameterFloatValue"
    bl_label = "Float"
    nl_category = "Values"
    nl_subcat = 'Simple'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicFloat, "")
        self.add_output(NodeSocketLogicFloat, "Float")

    def get_netlogic_class_name(self):
        return "ULSimpleValue"

    def get_input_names(self):
        return ["value"]

    def get_output_names(self):
        return ["OUT"]
