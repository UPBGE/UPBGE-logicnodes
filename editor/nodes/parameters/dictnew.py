from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicDictionary


@node_type
class LogicNodeDictNew(LogicNodeParameterType):
    bl_idname = "NLInitNewDict"
    bl_label = "Dictionary From Item"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicString, 'Key')
        self.add_input(NodeSocketLogicValue, '')
        self.add_output(NodeSocketLogicDictionary, 'Dictionary')
        LogicNodeParameterType.init(self, context)

    def get_output_names(self):
        return ['DICT']

    nl_class = "ULInitNewDict"

    def get_input_names(self):
        return ['key', 'val']
