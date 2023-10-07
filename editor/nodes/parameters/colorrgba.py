from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicColorRGBA


@node_type
class LogicNodeColorRGBA(LogicNodeParameterType):
    bl_idname = "NLParameterRGBANode"
    bl_label = "Color RGBA"
    nl_module = 'parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicColorRGBA, "Color")
        self.add_output(NodeSocketLogicColorRGBA, "Color")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULColorRGBA"

    def get_output_names(self):
        return ["OUTV"]

    def get_input_names(self):
        return ['color']
