from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicScene


@node_type
class LogicNodeGetScene(LogicNodeParameterType):
    bl_idname = "NLGetScene"
    bl_label = "Get Scene"
    nl_module = 'parameters'

    def init(self, context):
        self.add_output(NodeSocketLogicScene, 'Scene')
        LogicNodeParameterType.init(self, context)

    nl_class = "ULGetScene"

    def get_output_names(self):
        return ['OUT']
