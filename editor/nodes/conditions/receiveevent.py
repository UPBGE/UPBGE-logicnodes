from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicCondition
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeReceiveEvent(LogicNodeConditionType):
    bl_idname = "NLParameterReceiveMessage"
    bl_label = "Receive"
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULHandleEvent"

    search_tags = [
        ['Receive Event', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicString, "Subject")
        self.add_output(NodeSocketLogicCondition, "Received")
        self.add_output(NodeSocketLogicParameter, "Content")
        self.add_output(NodeSocketLogicCondition, "Messenger")
        LogicNodeConditionType.init(self, context)

    def get_input_names(self):
        return ['subject']

    def get_output_names(self):
        return ["OUT", 'BODY', 'TARGET']

