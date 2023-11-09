from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeSendNetworkMessage(LogicNodeActionType):
    bl_idname = "LogicNodeSendNetworkMessage"
    bl_label = "Send Data"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSendNetworkMessage"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicPython, "Server / Client")
        self.add_input(NodeSocketLogicParameter, "Data")
        self.add_input(NodeSocketLogicString, "Subject")
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return [
            "condition",
            "entity",
            'data',
            'subject'
        ]

    def get_output_names(self):
        return ['OUT']
