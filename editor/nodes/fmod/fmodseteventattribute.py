from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicBoolean
from bpy.props import EnumProperty


attrs = [
    ('', 'General', ''),
    ('position', 'Position', ''),
    ('orientation', 'Orientation', ''),
    ('pitch', 'Pitch', ''),
    ('volume', 'Volume', ''),
    ('', 'State', ''),
    ('paused', 'Paused', ''),
    ('timeline_position', 'Playback Position', ''),
]


@node_type
class LogicNodeFModSetEventAttribute(LogicNodeActionType):
    bl_idname = "LogicNodeFModSetEventAttribute"
    bl_label = "Set Event Instance Attribute"
    bl_width_default = 180
    bl_description = 'Set an attribute on an active event instance'
    nl_module = 'uplogic.nodes.fmod'
    nl_class = "FModSetEventAttributeNode"

    def update_draw(self, context=None):
        ipts = self.inputs
        ipts[2].enabled = self.mode in ['position', 'orientation']
        ipts[3].enabled = self.mode in ['paused', 'occluded', 'is_valid', 'is_virtual']
        ipts[4].enabled = self.mode in ['timeline_position']
        ipts[5].enabled = self.mode in ['pitch', 'volume']

    mode: EnumProperty(name='Attribute', items=attrs, update=update_draw, default='position')

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'mode', text='')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicPython, "Event Instance", 'event')
        self.add_input(NodeSocketLogicVectorXYZ, "Value", 'value')
        self.add_input(NodeSocketLogicBoolean, "Value", 'value')
        self.add_input(NodeSocketLogicInteger, "Value", 'value')
        self.add_input(NodeSocketLogicFloat, "Value", 'value')
        self.add_output(NodeSocketLogicCondition, "Done", 'DONE')
        self.add_output(NodeSocketLogicPython, "Event Instance", 'EVT')
        LogicNodeActionType.init(self, context)

    def get_attributes(self):
        return [('attribute', repr(self.mode))]
