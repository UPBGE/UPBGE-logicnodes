from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeParameterType
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
    ('occluded', 'Occluded', ''),
    ('playback_state', 'Playback State', ''),
    ('timeline_position', 'Playback Position', ''),
    ('', 'Debug', ''),
    ('is_valid', 'Is Valid', ''),
    ('is_virtual', 'Is Virtual', '')
]


@node_type
class LogicNodeFModGetEventAttribute(LogicNodeParameterType):
    bl_idname = "LogicNodeFModGetEventAttribute"
    bl_label = "Get Event Instance Attribute"
    bl_description = 'Get an attribute from an active event instance'
    bl_width_default = 180
    nl_module = 'uplogic.nodes.fmod'
    nl_class = "FModGetEventAttributeNode"

    def update_draw(self, context=None):
        opts = self.outputs
        for o in opts:
            o.enabled = False
        opts[1].enabled = self.mode in ['playback_state']
        opts[2].enabled = self.mode in ['position', 'orientation']
        opts[3].enabled = self.mode in ['paused', 'occluded', 'is_valid', 'is_virtual']
        opts[4].enabled = self.mode in ['timeline_position']
        opts[5].enabled = self.mode in ['pitch', 'volume']

    mode: EnumProperty(name='Attribute', items=attrs, update=update_draw, default='position')

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'mode', text='')

    def init(self, context):
        self.add_input(NodeSocketLogicPython, "Event Instance", 'event')
        self.add_output(NodeSocketLogicPython, "Event Instance", 'EVT')
        self.add_output(NodeSocketLogicPython, "Value", 'VALUE')
        self.add_output(NodeSocketLogicVectorXYZ, "Value", 'VALUE')
        self.add_output(NodeSocketLogicBoolean, "Value", 'VALUE')
        self.add_output(NodeSocketLogicInteger, "Value", 'VALUE')
        self.add_output(NodeSocketLogicFloat, "Value", 'VALUE')
        LogicNodeParameterType.init(self, context)

    def get_attributes(self):
        return [('attribute', repr(self.mode))]
