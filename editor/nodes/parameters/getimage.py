from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicImage


@node_type
class LogicNodeGetImage(LogicNodeParameterType):
    bl_idname = "NLGetImage"
    bl_label = "Get Image"
    bl_description = 'Image (ID)'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetImage"

    def init(self, context):
        self.add_input(NodeSocketLogicImage, "Image", 'image')
        self.add_output(NodeSocketLogicImage, 'Image', 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["image"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
