from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeListGetRandom(LogicNodeParameterType):
    bl_idname = "NLGetRandomListIndex"
    bl_label = "Get Random List Item"
    bl_description = 'Retrieve a random item from a list'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULListIndexRandom"

    def init(self, context):
        self.add_input(NodeSocketLogicList, "List", 'items')
        self.add_output(NodeSocketLogicParameter, "Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["items"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']