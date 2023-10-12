from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeVRHeadset(LogicNodeParameterType):
    bl_idname = "NLGetVRHeadsetValues"
    bl_label = "VR Headset"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_output(NodeSocketLogicVectorXYZ, "Position")
        self.add_output(NodeSocketLogicVectorXYZ, "Orientation")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULGetVRHeadsetValues"

    def get_output_names(self):
        return ['POS', 'ORI']
