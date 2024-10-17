from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicColorRGBA


@node_type
class LogicNodeColorRGBA(LogicNodeParameterType):
    bl_idname = "NLParameterRGBANode"
    bl_label = "Color RGBA"
    bl_description = 'Color with alpha channel'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULColorRGBA"

    def init(self, context):
        self.add_input(NodeSocketLogicColorRGBA, "Color", 'color')
        self.add_output(NodeSocketLogicColorRGBA, "Color", 'OUTV')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUTV"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['color']
