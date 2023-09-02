from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloatAngle
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicColorRGBA
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicUI
from ...sockets import NodeSocketLogicImage
from ...sockets import NodeSocketLogicFloatPositive
from ...enum_types import _ui_slider_types
from ...enum_types import _ui_boxlayout_types
from ...enum_types import _ui_halign_types
from ...enum_types import _ui_valign_types
from ....utilities import update_draw
from bpy.props import EnumProperty


@node_type
class LogicNodeCreateUISlider(LogicNodeActionType):
    bl_idname = "LogicNodeCreateUISlider"
    bl_label = "Create Slider"
    nl_category = "UI"
    nl_subcat = 'Widgets'
    nl_module = 'actions'
    slider_type: EnumProperty(items=_ui_slider_types, name='Type', update=update_draw)
    orientation_type: EnumProperty(items=_ui_boxlayout_types, name='Orientation', default='horizontal')
    halign_type: EnumProperty(items=_ui_halign_types, name='X')
    valign_type: EnumProperty(items=_ui_valign_types, name='Y')

    def init(self, context):
        LogicNodeActionType.init(self, context)
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicUI, "Parent")
        self.add_input(NodeSocketLogicBoolean, "Relative Position")
        self.add_input(NodeSocketLogicVectorXY, "")
        self.add_input(NodeSocketLogicBoolean, "Relative Size")
        self.add_input(NodeSocketLogicVectorXY, "", {'value_x': 200, 'value_y': 10})
        self.add_input(NodeSocketLogicFloatAngle, "Angle")
        self.add_input(NodeSocketLogicFloatPositive, "Bar Width", {'value': .5})
        self.add_input(NodeSocketLogicIntegerPositive, "Border Width", {'value': 1})
        self.add_input(NodeSocketLogicColorRGBA, "Border Color")
        self.add_input(NodeSocketLogicColorRGBA, "Bar Color", {'value': [.1, .1, .1, .5]})
        self.add_input(NodeSocketLogicColorRGBA, "Bar Hover Color", {'value': [.1, .1, .1, .7]})
        self.add_input(NodeSocketLogicImage, "Bar Texture", {'enabled': False})
        self.add_input(NodeSocketLogicFloatPositive, "Knob Size", {'value': 1.0})
        self.add_input(NodeSocketLogicColorRGBA, "Knob Color", {'value': [.7, .8, 1., 1.]})
        self.add_input(NodeSocketLogicColorRGBA, "Knob Hover Color")
        self.add_input(NodeSocketLogicImage, "Knob Texture", {'enabled': False})
        self.add_input(NodeSocketLogicIntegerPositive, "Steps")
        self.add_input(NodeSocketLogicBoolean, "Bar Control", {'value': True})
        self.add_output(NodeSocketLogicCondition, "Done")
        self.add_output(NodeSocketLogicUI, "Label")
        self.add_output(NodeSocketLogicFloat, "Slider Value")
        self.add_output(NodeSocketLogicVectorXY, "Knob Position")
        self.update_draw()

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'slider_type', text='')
        layout.prop(self, 'orientation_type', text='')
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')

    def update_draw(self):
        if len(self.inputs) < 16:
            return
        self.inputs[7].enabled = self.slider_type == '0'
        self.inputs[8].enabled = not self.inputs[7].enabled
        self.inputs[15].enabled = self.inputs[7].enabled

    def get_netlogic_class_name(self):
        return "ULCreateUISlider"

    def get_output_names(self):
        return ["OUT", 'WIDGET', 'VALUE', 'KNOB_POSITION']

    def get_attributes(self):
        return [
            ("orientation_type", lambda: f'"{self.orientation_type}"'),
            ("slider_type", lambda: f'"{self.slider_type}"'),
            ("halign_type", lambda: f'"{self.halign_type}"'),
            ("valign_type", lambda: f'"{self.valign_type}"')
        ]

    def get_input_names(self):
        return [
            "condition",
            'parent',
            'rel_pos',
            'pos',
            'rel_size',
            'size',
            'angle',
            'bar_width',
            'border_width',
            'border_color',
            'bar_color',
            'bar_hover_color',
            'bar_texture',
            'knob_size',
            'knob_color',
            'knob_hover_color',
            'knob_texture',
            'steps',
            'allow_bar_click'
        ]
