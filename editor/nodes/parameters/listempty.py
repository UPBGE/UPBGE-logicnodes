from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeListEmpty(LogicNodeParameterType):
    bl_idname = "NLInitEmptyList"
    bl_label = "New List"
    bl_description = 'Create a new list'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULInitEmptyList"

    def init(self, context):
        self.add_input(NodeSocketLogicInteger, 'Length', 'length')
        self.add_output(NodeSocketLogicList, 'List', 'LIST')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['LIST']

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['length']
