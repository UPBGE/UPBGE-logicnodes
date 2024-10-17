from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeVRHeadset(LogicNodeParameterType):
    bl_idname = "NLGetVRHeadsetValues"
    bl_label = "VR Headset"
    bl_description = 'World space data of a VR Headset'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetVRHeadsetValues"

    def init(self, context):
        self.add_output(NodeSocketLogicVectorXYZ, "Position", 'POS')
        self.add_output(NodeSocketLogicVectorXYZ, "Orientation", 'ORI')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['POS', 'ORI']
