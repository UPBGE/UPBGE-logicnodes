from bpy.types import Context, UILayout
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ..node import LogicNodeConditionType
from ..node import node_type
from bpy.props import BoolProperty


@node_type
class LogicNodeReceiveEvent(LogicNodeConditionType):
    bl_idname = "NLParameterReceiveMessage"
    bl_label = "Receive Event"
    bl_description = 'Check if an event is active'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULHandleEvent"

    def update_draw(self, context=None):
        self.inputs[1].enabled = self.use_target

    use_target: BoolProperty(
        name='Use Target',
        description='Check if the event is meant for a specified target',
        update=update_draw
    )

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'use_target')

    def init(self, context):
        self.add_input(NodeSocketLogicString, "Subject", 'subject')
        self.add_input(NodeSocketLogicObject, "Target", 'target')
        self.add_output(NodeSocketLogicCondition, "Received", 'OUT')
        self.add_output(NodeSocketLogicParameter, "Content", 'BODY')
        self.add_output(NodeSocketLogicObject, "Messenger", 'TARGET')
        LogicNodeConditionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['subject', 'target']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", 'BODY', 'TARGET']

