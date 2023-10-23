from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicColorRGB


@node_type
class LogicNodeColorRGB(LogicNodeParameterType):
    bl_idname = "NLParameterRGBNode"
    bl_label = "Color RGB"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicColorRGB, 'Color')
        self.add_output(NodeSocketLogicColorRGB, "Color")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULColorRGB"

    def get_output_names(self):
        return ["OUTV"]

    def get_input_names(self):
        return ['color']
