from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicDictionary


@node_type
class LogicNodeDictEmpty(LogicNodeParameterType):
    bl_idname = "NLInitEmptyDict"
    bl_label = "New Dictionary"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_output(NodeSocketLogicDictionary, 'Dictionary')
        LogicNodeParameterType.init(self, context)

    def get_output_names(self):
        return ['DICT']

    nl_class = "ULInitEmptyDict"
