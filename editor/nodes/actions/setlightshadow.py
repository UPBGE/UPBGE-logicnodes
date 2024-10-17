from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicLight
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetLightShadow(LogicNodeActionType):
    bl_idname = "NLSetLightShadowAction"
    bl_label = "Set Light Shadow"
    bl_description = 'Set if a light should cast shadows'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetLightShadow"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicLight, 'Light Object', 'lamp')
        self.add_input(NodeSocketLogicBoolean, 'Use Shadow', 'use_shadow')
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
            "use_shadow"
        ]
