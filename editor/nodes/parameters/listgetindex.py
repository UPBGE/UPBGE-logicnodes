from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeListGetIndex(LogicNodeParameterType):
    bl_idname = "NLGetListIndexNode"
    bl_label = "Get List Index"
    bl_description = 'Get the value stored at the given index'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULListIndex"

    def init(self, context):
        self.add_input(NodeSocketLogicList, "List", 'items')
        self.add_input(NodeSocketLogicInteger, "Index", 'index')
        self.add_output(NodeSocketLogicParameter, "Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["items", "index"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
