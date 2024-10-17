from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetEeveeSSR(LogicNodeActionType):
    bl_idname = "NLSetEeveeSSR"
    bl_label = "Set SSR"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetEeveeSSR"
    deprecated = True
    deprecation_message = 'This node will be removed in a future update.'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicBoolean, 'Use SSR')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return [
            "condition",
            "value"
        ]
