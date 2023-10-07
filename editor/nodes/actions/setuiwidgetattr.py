from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicUI
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicColorRGBA
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicFont
from ...sockets import NodeSocketLogicImage
from ...sockets import NodeSocketLogicFloatAngle
from ...enum_types import _writeable_widget_attrs
from bpy.props import EnumProperty


@node_type
class LogicNodeSetUIWidgetAttr(LogicNodeActionType):
    bl_idname = "LogicNodeSetUIWidgetAttr"
    bl_label = "Set Widget Attribute"
    nl_module = 'actions'

    def update_draw(self, context=None):
        if not self.ready:
            return
        attr = self.widget_attr
        self.inputs[2].enabled = attr in ['show', 'use_clipping', 'wrap', 'shadow']
        self.inputs[3].enabled = attr in ['bg_color', 'border_color', 'shadow_color', 'font_color', 'hover_color']
        self.inputs[4].enabled = attr in ['opacity', 'font_opacity']
        self.inputs[5].enabled = attr in ['pos', 'size', 'shadow_offset']
        self.inputs[6].enabled = attr in ['halign', 'valign', 'text', 'text_halign', 'text_valign', 'orientation']
        self.inputs[7].enabled = attr in ['spacing', 'font_size', 'icon', 'rows', 'cols', 'border_width']
        self.inputs[8].enabled = attr in ['width', 'height', 'line_height']
        self.inputs[9].enabled = attr in ['font']
        self.inputs[10].enabled = attr in ['texture']
        self.inputs[11].enabled = attr in ['angle']

    widget_attr: EnumProperty(items=_writeable_widget_attrs, name='', update=update_draw)

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicUI, "Widget")
        self.add_input(NodeSocketLogicBoolean, "")
        self.add_input(NodeSocketLogicColorRGBA, "", {'enabled': False})
        self.add_input(NodeSocketLogicFloatFactor, "", {'enabled': False})
        self.add_input(NodeSocketLogicVectorXY, "", {'enabled': False})
        self.add_input(NodeSocketLogicString, "", {'enabled': False})
        self.add_input(NodeSocketLogicInteger, "", {'enabled': False})
        self.add_input(NodeSocketLogicFloat, "", {'enabled': False})
        self.add_input(NodeSocketLogicFont, "", {'enabled': False})
        self.add_input(NodeSocketLogicImage, "", {'enabled': False})
        self.add_input(NodeSocketLogicFloatAngle, "", {'enabled': False})
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def get_attributes(self):
        return [("widget_attr", f'"{self.widget_attr}"')]

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'widget_attr', text='')

    nl_class = "ULSetUIWidgetAttr"

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return [
            "condition",
            'widget',
            'bool_value',
            'color_value',
            'alpha_value',
            'vec2_value',
            'str_value',
            'int_value',
            'float_value',
            'font_value',
            'img_value',
            'angle_value'
        ]
