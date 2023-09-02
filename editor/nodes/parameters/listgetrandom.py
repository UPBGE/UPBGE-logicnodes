from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeListGetRandom(LogicNodeParameterType):
    bl_idname = "NLGetRandomListIndex"
    bl_label = "Get Random Item"
    nl_category = "Data"
    nl_subcat = 'List'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicList, "List")# .display_shape = 'SQUARE'
        self.add_output(NodeSocketLogicParameter, "Value")

    def get_netlogic_class_name(self):
        return "ULListIndexRandom"

    def get_input_names(self):
        return ["items"]

    def get_output_names(self):
        return ['OUT']