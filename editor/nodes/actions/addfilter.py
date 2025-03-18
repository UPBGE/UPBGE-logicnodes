from bpy.types import NodeLink
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicColorRGB
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicFloat
from bpy.props import EnumProperty


filter_types = [
    ('0', 'FXAA', 'Fast Anti-Aliasing'),
    ('1', 'HBAO', 'Horizon-Based Ambient Occlusion'),
    ('2', 'SSAO', 'Screen-Space Ambient Occlusion'),
    ('3', 'Vignette', 'Fade to color at screen edges'),
    ('4', 'Brightness', 'Overall brightness'),
    ('5', 'Chromatic Aberration', 'Lens light bending effect'),
    ('6', 'Grayscale', 'Convert image to grayscale'),
    ('7', 'Levels', 'Control color levels'),
    ('8', 'Mist', 'Classic depth fog implementation'),
    ('9', 'Blur', 'Simple blur covering the whole screen')
]


@node_type
class LogicNodeAddFilter(LogicNodeActionType):
    bl_idname = "NLAddFilter"
    bl_label = "Add Filter"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULAddFilter"
    bl_description = 'Apply a 2D filter on the rendered image'

    def update_draw(self, context=None):
        if not self.ready:
            return
        ftype = int(self.filter_type)
        self.inputs[2].enabled = ftype == 4
        self.inputs[3].enabled = ftype == 8
        self.inputs[4].enabled = self.inputs[3].enabled
        self.inputs[5].enabled = ftype in [3, 5, 6, 8, 2, 1, 9]
        self.inputs[6].enabled = ftype in [3, 7, 8]

    filter_type: EnumProperty(
        items=filter_types,
        name='Filter',
        description='2D Filters modify the image rendered by EEVEE',
        default='0',
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

    def insert_link(self, link: NodeLink) -> None:
        self.outputs[0].display_shape = self.inputs[0].display_shape

    def draw_buttons(self, context, layout):
        layout.prop(self, "filter_type")

    def get_input_names(self):  # XXX Remove for 5.0
        return ['condition', 'pass_idx', 'brightness', 'start', 'density', 'power', 'color']

    def get_attributes(self):
        return [("filter_type", self.filter_type)]

    def get_output_names(self):  # XXX Remove for 5.0
        return ["OUT"]
