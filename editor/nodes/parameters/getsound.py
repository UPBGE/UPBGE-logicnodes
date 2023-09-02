from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicSoundFile


@node_type
class LogicNodeGetSound(LogicNodeParameterType):
    bl_idname = "NLGetSound"
    bl_label = "Get Sound"
    bl_icon = 'FILE_SOUND'
    nl_category = "File"
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicSoundFile, "Sound File")
        self.add_output(NodeSocketLogicSoundFile, 'Sound File')

    def get_netlogic_class_name(self):
        return "ULGetSound"

    def get_input_names(self):
        return ["sound"]

    def get_output_names(self):
        return ['OUT']
