from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicDictionary


@node_type
class LogicNodeSendNetworkMessage(LogicNodeActionType):
    bl_idname = "LogicNodeSendNetworkMessage"
    bl_label = "Send Data"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSendNetworkMessage"
    bl_description = 'Send data through an established connection'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicPython, "Server / Client", 'entity')
        self.add_input(NodeSocketLogicDictionary, "Data", 'data')
        self.add_input(NodeSocketLogicString, "Subject", 'subject')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "entity",
            'data',
            'subject'
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
