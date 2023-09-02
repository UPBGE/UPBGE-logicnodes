from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicInteger


@node_type
class LogicNodeInteger(LogicNodeParameterType):
    bl_idname = "NLParameterIntValue"
    bl_label = "Integer"
    nl_category = "Values"
    nl_subcat = 'Simple'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicInteger, "")
        self.add_output(NodeSocketLogicInteger, "Int")

    def get_netlogic_class_name(self):
        return "ULSimpleValue"

    def get_input_names(self):
        return ["value"]

    def get_output_names(self):
        return ["OUT"]
