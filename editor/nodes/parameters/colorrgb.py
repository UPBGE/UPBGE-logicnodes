from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicColorRGB


@node_type
class LogicNodeColorRGB(LogicNodeParameterType):
    bl_idname = "NLParameterRGBNode"
    bl_label = "Color RGB"
    bl_description = 'Color with no alpha channel'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULColorRGB"

    def init(self, context):
        self.add_input(NodeSocketLogicColorRGB, 'Color', 'color')
        self.add_output(NodeSocketLogicColorRGB, "Color", 'OUTV')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUTV"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['color']
