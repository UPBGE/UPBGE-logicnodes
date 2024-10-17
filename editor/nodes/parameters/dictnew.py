from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicDictionary


@node_type
class LogicNodeDictNew(LogicNodeParameterType):
    bl_idname = "NLInitNewDict"
    bl_label = "Dictionary From Item"
    bl_description = 'New dictionary with an inital {key: value} pair'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULInitNewDict"

    def init(self, context):
        self.add_input(NodeSocketLogicString, 'Key', 'key')
        self.add_input(NodeSocketLogicValue, '', 'val')
        self.add_output(NodeSocketLogicDictionary, 'Dictionary', 'DICT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['DICT']

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['key', 'val']
