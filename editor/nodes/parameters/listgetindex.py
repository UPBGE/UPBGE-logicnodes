from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeListGetIndex(LogicNodeParameterType):
    bl_idname = "NLGetListIndexNode"
    bl_label = "Get List Index"
    nl_module = 'parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicList, "List")
        self.add_input(NodeSocketLogicInteger, "Index")
        self.add_output(NodeSocketLogicParameter, "Value")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULListIndex"

    def get_input_names(self):
        return ["items", "index"]

    def get_output_names(self):
        return ['OUT']
