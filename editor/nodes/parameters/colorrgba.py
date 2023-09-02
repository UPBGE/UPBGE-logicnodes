from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicColorRGBA


@node_type
class LogicNodeColorRGBA(LogicNodeParameterType):
    bl_idname = "NLParameterRGBANode"
    bl_label = "Color RGBA"
    nl_category = "Values"
    nl_subcat = 'Vectors'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicColorRGBA, "Color")
        self.add_output(NodeSocketLogicColorRGBA, "Color")

    def get_netlogic_class_name(self):
        return "ULColorRGBA"

    def get_output_names(self):
        return ["OUTV"]

    def get_input_names(self):
        return ['color']
