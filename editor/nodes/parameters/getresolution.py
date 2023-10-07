from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicVectorXY


@node_type
class LogicNodeGetResolution(LogicNodeParameterType):
    bl_idname = "NLGetResolution"
    bl_label = "Get Resolution"
    nl_module = 'parameters'

    def init(self, context):
        self.add_output(NodeSocketLogicParameter, "Width")
        self.add_output(NodeSocketLogicParameter, "Height")
        self.add_output(NodeSocketLogicVectorXY, "Resolution")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULGetResolution"

    def get_output_names(self):
        return ['WIDTH', 'HEIGHT', 'RES']
