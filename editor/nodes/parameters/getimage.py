from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicImage


@node_type
class LogicNodeGetImage(LogicNodeParameterType):
    bl_idname = "NLGetImage"
    bl_label = "Get Image"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetImage"

    def init(self, context):
        self.add_input(NodeSocketLogicImage, "Image")
        self.add_output(NodeSocketLogicImage, 'Image')
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["image"]

    def get_output_names(self):
        return ['OUT']
