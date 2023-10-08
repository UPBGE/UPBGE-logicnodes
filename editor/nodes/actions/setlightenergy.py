from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicLight
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeSetLightEnergy(LogicNodeActionType):
    bl_idname = "NLSetLightEnergyAction"
    bl_label = "Set Light Energy"
    nl_module = 'actions'
    nl_class = "ULSetLightEnergy"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicLight, 'Light Object')
        self.add_input(NodeSocketLogicFloat, 'Energy')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return [
            "condition",
            "lamp",
            "energy"
        ]
