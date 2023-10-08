from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetEeveeAO(LogicNodeActionType):
    bl_idname = "NLSetEeveeAO"
    bl_label = "Set Ambient Occlusion"
    nl_module = 'actions'
    nl_class = "ULSetEeveeAO"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicBoolean, 'Use AO')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return [
            "condition",
            "value"
        ]
