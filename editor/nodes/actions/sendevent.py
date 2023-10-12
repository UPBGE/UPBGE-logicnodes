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

    search_tags = [
        ['Send Event', {}],
        ['Dispatch Event', {}]
    ]

    def update_draw(self, context=None):
        if not self.ready:
            return
        adv = [2, 3]
        for x in adv:
            self.inputs[x].enabled = self.advanced

    advanced: BoolProperty(
        name='Advanced',
        description='Show advanced options for this node. Hidden sockets will not be reset',
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicString, "Subject")
        self.add_input(NodeSocketLogicValueOptional, "Content")
        self.add_input(NodeSocketLogicObject, "Messenger", {'use_owner': True})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'advanced', text='Advanced', icon='SETTINGS')

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "subject", "body", 'target']
