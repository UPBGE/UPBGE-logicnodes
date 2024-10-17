from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicScene


@node_type
class LogicNodeGetScene(LogicNodeParameterType):
    bl_idname = "NLGetScene"
    bl_label = "Get Scene"
    bl_description = 'The current scene'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetScene"

    def init(self, context):
        self.add_output(NodeSocketLogicScene, 'Scene', 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
