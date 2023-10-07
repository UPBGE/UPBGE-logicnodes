from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicLight
from ...sockets import NodeSocketLogicColorRGB


@node_type
class LogicNodeGetLightColor(LogicNodeParameterType):
    bl_idname = "NLGetLightColorAction"
    bl_label = "Get Light Color"
    nl_module = 'parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicLight, "Light Object")
        self.add_output(NodeSocketLogicColorRGB, 'Color')
        LogicNodeParameterType.init(self, context)

    def get_output_names(self):
        return ['COLOR']

    nl_class = "ULGetLightColor"

    def get_input_names(self):
        return ["lamp"]
