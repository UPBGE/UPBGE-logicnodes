from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicBitMask
from bpy.props import BoolProperty


@node_type
class LogicNodeFModStartEvent(LogicNodeActionType):
    bl_idname = "LogicNodeFModStartEvent"
    bl_label = "Start Event Instance"
    bl_width_default = 180
    bl_description = 'Start a new event instance from a loaded .bank file'
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
        self.add_input(NodeSocketLogicBitMask, "Occlusion Mask", 'mask')
        self.add_input(NodeSocketLogicString, "", 'channel', {'default_value': 'default'})
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        self.add_output(NodeSocketLogicPython, "Event Instance", 'EVT')
        LogicNodeActionType.init(self, context)
