from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicLight
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeGetLightEnergy(LogicNodeParameterType):
    bl_idname = "NLGetLightEnergy"
    bl_label = "Get Light Energy"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicLight, "Light Object")
        self.add_output(NodeSocketLogicFloat, 'Enery')
        LogicNodeParameterType.init(self, context)

    def get_output_names(self):
        return ['ENERGY']

    nl_class = "ULGetLightEnergy"

    def get_input_names(self):
        return ["lamp"]
