from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeListEmpty(LogicNodeParameterType):
    bl_idname = "NLInitEmptyList"
    bl_label = "Create Empty List"
    nl_module = 'parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicInteger, 'Length')
        self.add_output(NodeSocketLogicList, 'List')
        LogicNodeParameterType.init(self, context)

    def get_output_names(self):
        return ['LIST']

    nl_class = "ULInitEmptyList"

    def get_input_names(self):
        return ['length']
