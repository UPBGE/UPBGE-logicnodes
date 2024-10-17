from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicLight
from ...sockets import NodeSocketLogicColorRGB


@node_type
class LogicNodeGetLightColor(LogicNodeParameterType):
    bl_idname = "NLGetLightColorAction"
    bl_label = "Get Light Color"
    bl_description = 'Color of a light source'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetLightColor"

    def init(self, context):
        self.add_input(NodeSocketLogicLight, "Light Object", 'lamp')
        self.add_output(NodeSocketLogicColorRGB, 'Color', 'COLOR')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['COLOR']

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["lamp"]
