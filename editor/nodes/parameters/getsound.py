from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicSoundFile


@node_type
class LogicNodeGetSound(LogicNodeParameterType):
    bl_idname = "NLGetSound"
    bl_label = "Get Sound"
    bl_description = 'Sound (ID)'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetSound"

    def init(self, context):
        self.add_input(NodeSocketLogicSoundFile, "Sound File", 'sound')
        self.add_output(NodeSocketLogicSoundFile, 'Sound File', 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["sound"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
