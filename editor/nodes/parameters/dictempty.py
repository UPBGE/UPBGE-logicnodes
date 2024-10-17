from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicDictionary


@node_type
class LogicNodeDictEmpty(LogicNodeParameterType):
    bl_idname = "NLInitEmptyDict"
    bl_label = "New Dictionary"
    bl_description = 'An empty dictionary'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULInitEmptyDict"

    def init(self, context):
        self.add_output(NodeSocketLogicDictionary, 'Dictionary', 'DICT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['DICT']
