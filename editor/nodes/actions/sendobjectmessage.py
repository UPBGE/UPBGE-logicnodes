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
    bl_description = 'Send a message that can be received by logic bricks'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "From", 'from_obj')
        self.add_input(NodeSocketLogicObject, "To", 'to_obj', {'allow_owner': False})
        self.add_input(NodeSocketLogicString, "Subject", 'subject')
        self.add_input(NodeSocketLogicString, "Body", 'body')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['condition', 'from_obj', 'to_obj', 'subject', 'body']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
