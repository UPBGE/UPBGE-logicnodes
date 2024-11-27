from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicValueOptional
from ...sockets import NodeSocketLogicObject
from bpy.props import BoolProperty


@node_type
class LogicNodeSendEvent(LogicNodeActionType):
    bl_idname = "NLActionCreateMessage"
    bl_label = "Send Event"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULDispatchEvent"
    bl_description = 'Dispatch an event that can be received elsewhere'

    def update_draw(self, context=None):
        if not self.ready:
            return
        adv = [2, 3]
        for x in adv:
            self.inputs[x].enabled = self.advanced
        self.inputs[4].enabled = self.use_target

    advanced: BoolProperty(
        name='Use Content',
        description='Send additional information along with the event',
        update=update_draw
    )
    use_target: BoolProperty(
        name='Use Target',
        description='Only send the event to a specific target',
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicString, "Subject", 'subject')
        self.add_input(NodeSocketLogicValueOptional, "Content", 'body')
        self.add_input(NodeSocketLogicObject, "Messenger", 'messenger', {'use_owner': True})
        self.add_input(NodeSocketLogicObject, "Target", 'target')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'advanced')
        layout.prop(self, 'use_target')

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "subject", "body", 'messenger', 'target']
