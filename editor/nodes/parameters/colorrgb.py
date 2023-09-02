from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicColorRGB


@node_type
class LogicNodeColorRGB(LogicNodeParameterType):
    bl_idname = "NLParameterRGBNode"
    bl_label = "Color RGB"
    nl_category = "Values"
    nl_subcat = 'Vectors'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicColorRGB, 'Color')
        self.add_output(NodeSocketLogicColorRGB, "Color")

    def get_netlogic_class_name(self):
        return "ULColorRGB"

    def get_output_names(self):
        return ["OUTV"]

    def get_input_names(self):
        return ['color']
