from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFloatPositive


@node_type
class LogicNodeSetExposure(LogicNodeActionType):
    bl_idname = "NLSetExposureAction"
    bl_label = "Set Exposure"
    bl_description = 'Set the scene exposure'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetExposure"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicFloatPositive, 'Exposure', 'value')
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
