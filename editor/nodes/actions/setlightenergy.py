from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicLight
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeSetLightEnergy(LogicNodeActionType):
    bl_idname = "NLSetLightEnergyAction"
    bl_label = "Set Light Power"
    bl_description = 'Set the emission strength of a light'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetLightEnergy"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicLight, 'Light Object', 'lamp')
        self.add_input(NodeSocketLogicFloat, 'Power', 'energy')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "lamp",
            "energy"
        ]
