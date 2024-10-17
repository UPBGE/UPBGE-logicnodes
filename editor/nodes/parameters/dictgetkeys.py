from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicDictionary
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeDictGetKeys(LogicNodeParameterType):
    bl_idname = "LogicNodeDictGetKeys"
    bl_label = 'Get Dictionary Keys'
    bl_description = 'List of keys in a dictionary'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "DictGetKeysNode"

    def init(self, context):
        self.add_input(NodeSocketLogicDictionary, "Dictionary", 'dict')
        self.add_output(NodeSocketLogicParameter, "Keys", 'KEYS', shape='SQUARE')
        LogicNodeParameterType.init(self, context)
