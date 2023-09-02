from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicImage


@node_type
class LogicNodeGetImage(LogicNodeParameterType):
    bl_idname = "NLGetImage"
    bl_label = "Get Image"
    bl_icon = 'IMAGE_DATA'
    nl_category = "File"
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicImage, "Image")
        self.add_output(NodeSocketLogicImage, 'Image')

    def get_netlogic_class_name(self):
        return "ULGetImage"

    def get_input_names(self):
        return ["image"]

    def get_output_names(self):
        return ['OUT']
