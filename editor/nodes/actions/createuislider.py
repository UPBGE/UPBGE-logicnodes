from ..node import node_type
from ..node import LogicNodeUIType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloatAngle
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicColorRGBA
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicUI
from ...sockets import NodeSocketLogicImage
from ...sockets import NodeSocketLogicFloatPositive
from ...enum_types import _ui_slider_types
from ...enum_types import _ui_boxlayout_types
from ...enum_types import _ui_halign_types
from ...enum_types import _ui_valign_types
from bpy.props import EnumProperty
from ..node import WIDGETS
import math


@node_type
class LogicNodeCreateUISliderWidget(LogicNodeUIType):
    bl_idname = "LogicNodeCreateUISliderWidget"
    bl_label = "Create Slider"
    bl_description = 'Create a new interactible slider widget'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULCreateUISlider"

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.inputs[11].enabled = self.slider_type != '0'
        self.inputs[7].enabled = not self.inputs[11].enabled
        self.inputs[12].enabled = self.inputs[11].enabled
        
        w = WIDGETS.get(self, None)
        if w is None:
            return
        if w.__class__ is not self.get_ui_class():
            parent = w.parent
            w.remove()
            del WIDGETS[self]
            w = WIDGETS[self] = self.get_ui_class()()
            w.update = self.update_widget
            parent.add_widget(w)

    def get_ui_class(self):
        from uplogic.ui.preview.slider import SliderPreview, FrameSliderPreview, ProgressSliderPreview
        return {
            '0': SliderPreview,
            '1': FrameSliderPreview,
            '2': ProgressSliderPreview
        }.get(self.slider_type)

    slider_type: EnumProperty(items=_ui_slider_types, name='Type', update=update_draw)
    orientation_type: EnumProperty(items=_ui_boxlayout_types, name='Orientation', default='horizontal')
    halign_type: EnumProperty(items=_ui_halign_types, name='X')
    valign_type: EnumProperty(items=_ui_valign_types, name='Y')

    def update_widget(self):
        w = WIDGETS.get(self, None)
        if w is None:
            return
        ipts = self.inputs
        w.relative['pos'] = ipts[2].default_value
        w.pos = ipts[3].default_value
        w.relative['size'] = ipts[4].default_value
        w.size = ipts[5].default_value
        w.angle = math.degrees(ipts[6].default_value)
        w.bar_width = ipts[7].default_value
        w.bar_color = ipts[8].default_value
        w.border_width = ipts[11].default_value
        w.border_color = ipts[12].default_value
        w.halign = self.halign_type
        w.valign = self.valign_type
        w.orientation = self.orientation_type
        w.knob_size = ipts[13].default_value
        w.knob_color = ipts[14].default_value
        w.value = ipts[17].default_value

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicUI, "Parent", 'parent')
        self.add_input(NodeSocketLogicBoolean, "Relative Position", 'rel_pos')
        self.add_input(NodeSocketLogicVectorXY, "", 'pos')
        self.add_input(NodeSocketLogicBoolean, "Relative Size", 'rel_size')
        self.add_input(NodeSocketLogicVectorXY, "", 'size', {'default_value': (200., 10.)})
        self.add_input(NodeSocketLogicFloatAngle, "Angle", 'angle')
        self.add_input(NodeSocketLogicFloatPositive, "Bar Width", 'bar_width', {'default_value': .5})
        self.add_input(NodeSocketLogicColorRGBA, "Bar Color", 'bar_color', {'default_value': (.1, .1, .1, .5)})
        self.add_input(NodeSocketLogicColorRGBA, "Bar Hover Color", 'bar_hover_color', {'default_value': (.1, .1, .1, .7)})
        self.add_input(NodeSocketLogicImage, "Bar Texture", 'bar_texture', {'enabled': False})
        self.add_input(NodeSocketLogicIntegerPositive, "Border Width", 'border_width', {'default_value': 1})
        self.add_input(NodeSocketLogicColorRGBA, "Border Color", 'border_color')
        self.add_input(NodeSocketLogicFloatPositive, "Knob Size", 'knob_size', {'default_value': 1.0})
        self.add_input(NodeSocketLogicColorRGBA, "Knob Color", 'knob_color', {'default_value': (.7, .8, 1., 1.)})
        self.add_input(NodeSocketLogicColorRGBA, "Knob Hover Color", 'knob_hover_color')
        self.add_input(NodeSocketLogicImage, "Knob Texture", 'knob_texture', {'enabled': False})
        self.add_input(NodeSocketLogicFloatFactor, "Initial Value", 'initial_value')
        self.add_input(NodeSocketLogicIntegerPositive, "Steps", 'steps')
        self.add_input(NodeSocketLogicBoolean, "Bar Control", 'allow_bar_click', {'default_value': True})
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        self.add_output(NodeSocketLogicUI, "Slider", 'WIDGET')
        self.add_output(NodeSocketLogicFloat, "Slider Value", 'VALUE')
        self.add_output(NodeSocketLogicVectorXY, "Knob Position", 'KNOB_POSITION')
        LogicNodeUIType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'slider_type', text='')
        layout.prop(self, 'orientation_type', text='')
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')

    def get_attributes(self):
        return [
            ("orientation_type", repr(self.orientation_type)),
            ("slider_type", repr(self.slider_type)),
            ("halign_type", repr(self.halign_type)),
            ("valign_type", repr(self.valign_type))
        ]
