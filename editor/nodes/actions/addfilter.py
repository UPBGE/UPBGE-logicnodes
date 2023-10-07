from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicColorRGB
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicFloat
from ...enum_types import _enum_2d_filters
from bpy.props import EnumProperty


@node_type
class LogicNodeAddFilter(LogicNodeActionType):
    bl_idname = "NLAddFilter"
    bl_label = "Add Filter"
    nl_module = 'actions'

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.inputs[2].enabled = self.filter_type == 'BRIGHTNESS'
        self.inputs[3].enabled = self.filter_type == 'MIST'
        self.inputs[4].enabled = self.inputs[3].enabled
        self.inputs[5].enabled = self.filter_type in ['VIGNETTE', 'CHROMAB', 'GRAYSCALE', 'MIST', 'SSAO', 'HBAO']
        self.inputs[6].enabled = self.filter_type in ['VIGNETTE', 'LEVELS', 'MIST']

    filter_type: EnumProperty(
        items=_enum_2d_filters,
        name='Filter',
        description='2D Filters modify the image rendered by EEVEE',
        default='FXAA',
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Pass Index')
        self.add_input(NodeSocketLogicFloat, 'Brightness', {'value': 1.0})
        self.add_input(NodeSocketLogicFloat, 'Start', {'value': .1})
        self.add_input(NodeSocketLogicFloat, 'Density', {'value': .5})
        self.add_input(NodeSocketLogicFloat, 'Power', {'value': 1.0})
        self.add_input(NodeSocketLogicColorRGB, 'Color')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "filter_type")

    def get_input_names(self):
        return ['condition', 'pass_idx', 'brightness', 'start', 'density', 'power', 'color', 'end']

    def get_attributes(self):
        return [
            ("filter_type", f'"{self.filter_type}"')
        ]

    def get_output_names(self):
        return ["OUT"]

    nl_class = "ULAddFilter"
