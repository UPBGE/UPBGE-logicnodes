from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicLight
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeGetLightEnergy(LogicNodeParameterType):
    bl_idname = "NLGetLightEnergy"
    bl_label = "Get Light Power"
    bl_description = 'Emission strength of a light source'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetLightEnergy"

    def init(self, context):
        self.add_input(NodeSocketLogicLight, "Light Object", 'lamp')
        self.add_output(NodeSocketLogicFloat, 'Power', 'ENERGY')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['ENERGY']

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["lamp"]
