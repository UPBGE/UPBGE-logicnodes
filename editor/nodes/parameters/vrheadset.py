from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeVRHeadset(LogicNodeParameterType):
    bl_idname = "NLGetVRHeadsetValues"
    bl_label = "VR Headset"
    nl_category = "Input"
    nl_subcat = 'VR'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_output(NodeSocketLogicVectorXYZ, "Position")
        self.add_output(NodeSocketLogicVectorXYZ, "Orientation")

    def get_netlogic_class_name(self):
        return "ULGetVRHeadsetValues"

    def get_output_names(self):
        return ['POS', 'ORI']
