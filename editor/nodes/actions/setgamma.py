from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFloatPositive


@node_type
class LogicNodeSetGamma(LogicNodeActionType):
    bl_idname = "NLSetGammaAction"
    bl_label = "Set Gamma"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetGamma"
    bl_description = 'Set the scene gamma'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicFloatPositive, 'Gamma', 'value')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "value"
        ]
