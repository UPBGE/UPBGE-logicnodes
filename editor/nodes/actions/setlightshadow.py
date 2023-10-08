from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicLight
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetLightShadow(LogicNodeActionType):
    bl_idname = "NLSetLightShadowAction"
    bl_label = "Set Light Shadow"
    nl_module = 'actions'
    nl_class = "ULSetLightShadow"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicLight, 'Light Object')
        self.add_input(NodeSocketLogicBoolean, 'Use Shadow')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return [
            "condition",
            "lamp",
            "use_shadow"
        ]
