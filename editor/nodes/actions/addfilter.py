from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicColorRGB
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicFloat
from bpy.props import EnumProperty


filter_types = [
    ('FXAA', 'FXAA', 'Fast Anti-Aliasing'),
    ('HBAO', 'HBAO', 'Horizon-Based Ambient Occlusion'),
    ('SSAO', 'SSAO', 'Screen-Space Ambient Occlusion'),
    ('VIGNETTE', 'Vignette', 'Fade to color at screen edges'),
    ('BRIGHTNESS', 'Brightness', 'Overall brightness'),
    ('CHROMAB', 'Chromatic Aberration', 'Lens light bending effect'),
    ('GRAYSCALE', 'Grayscale', 'Convert image to grayscale'),
    ('LEVELS', 'Levels', 'Control color levels'),
    ('MIST', 'Mist', 'Classic depth fog implementation')
]


@node_type
class LogicNodeAddFilter(LogicNodeActionType):
    bl_idname = "NLAddFilter"
    bl_label = "Add Filter"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULAddFilter"

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.inputs[2].enabled = self.filter_type == 'BRIGHTNESS'
        self.inputs[3].enabled = self.filter_type == 'MIST'
        self.inputs[4].enabled = self.inputs[3].enabled
        self.inputs[5].enabled = self.filter_type in ['VIGNETTE', 'CHROMAB', 'GRAYSCALE', 'MIST', 'SSAO', 'HBAO']
        self.inputs[6].enabled = self.filter_type in ['VIGNETTE', 'LEVELS', 'MIST']

    filter_type: EnumProperty(
        items=filter_types,
        name='Filter',
        description='2D Filters modify the image rendered by EEVEE',
        default='FXAA',
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition', {'show_prop': True})
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Pass Index', 'pass_idx')
        self.add_input(NodeSocketLogicFloat, 'Brightness', 'brightness', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloat, 'Start', 'start', {'default_value': .1})
        self.add_input(NodeSocketLogicFloat, 'Density', 'density', {'default_value': .5})
        self.add_input(NodeSocketLogicFloat, 'Power', 'power', {'default_value': 1.0})
        self.add_input(NodeSocketLogicColorRGB, 'Color', 'color')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "filter_type")

    def get_input_names(self):  # XXX Remove for 4.0
        return ['condition', 'pass_idx', 'brightness', 'start', 'density', 'power', 'color']

    def get_attributes(self):
        return [("filter_type", f'"{self.filter_type}"')]

    def get_output_names(self):  # XXX Remove for 4.0
        return ["OUT"]
