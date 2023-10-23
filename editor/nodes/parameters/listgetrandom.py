from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeListGetRandom(LogicNodeParameterType):
    bl_idname = "NLGetRandomListIndex"
    bl_label = "Get Random List Item"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicList, "List")
        self.add_output(NodeSocketLogicParameter, "Value")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULListIndexRandom"

    def get_input_names(self):
        return ["items"]

    def get_output_names(self):
        return ['OUT']