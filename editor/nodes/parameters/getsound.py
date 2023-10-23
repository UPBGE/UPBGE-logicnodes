from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicSoundFile


@node_type
class LogicNodeGetSound(LogicNodeParameterType):
    bl_idname = "NLGetSound"
    bl_label = "Get Sound"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetSound"

    def init(self, context):
        self.add_input(NodeSocketLogicSoundFile, "Sound File")
        self.add_output(NodeSocketLogicSoundFile, 'Sound File')
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["sound"]

    def get_output_names(self):
        return ['OUT']
