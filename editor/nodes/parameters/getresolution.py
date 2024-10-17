from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicVectorXY


@node_type
class LogicNodeGetResolution(LogicNodeParameterType):
    bl_idname = "NLGetResolution"
    bl_label = "Get Resolution"
    bl_description = 'The current game window resolution'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetResolution"

    def init(self, context):
        self.add_output(NodeSocketLogicParameter, "Width", 'WIDTH')
        self.add_output(NodeSocketLogicParameter, "Height", 'HEIGHT')
        self.add_output(NodeSocketLogicVectorXY, "Resolution", 'RES')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['WIDTH', 'HEIGHT', 'RES']
