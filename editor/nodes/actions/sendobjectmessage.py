from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeSendObjectMessage(LogicNodeActionType):
    """Send a message to be received by an object's 'Message' Logic Brick"""
    bl_idname = "NLActionSendMessage"
    bl_label = "Send Message"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSendMessage"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "From")
        self.add_input(NodeSocketLogicObject, "To", None, {'allow_owner': False})
        self.add_input(NodeSocketLogicString, "Subject")
        self.add_input(NodeSocketLogicString, "Body")
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ['condition', 'from_obj', 'to_obj', 'subject', 'body']

    def get_output_names(self):
        return ['OUT']
