from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicPython
from bpy.props import BoolProperty


@node_type
class LogicNodeFModStartEvent(LogicNodeActionType):
    bl_idname = "LogicNodeFModStartEvent"
    bl_label = "FMod Start Event"
    nl_module = 'uplogic.nodes.fmod'
    nl_class = "FModStartEventNode"

    def update_draw(self, context=None):
        self.inputs[2].enabled = not self.mode
        self.inputs[3].enabled = self.mode

    mode: BoolProperty(name='Speaker Mode', update=update_draw)

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'mode')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicString, "Event", 'event')
        self.add_input(NodeSocketLogicVectorXYZ, "Position", 'source')
        self.add_input(NodeSocketLogicObject, "Speaker", 'source')
        self.add_input(NodeSocketLogicString, "Channel", 'channel', {'default_value': 'default'})
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        self.add_output(NodeSocketLogicPython, "Event", 'EVT')
        LogicNodeActionType.init(self, context)
