from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicUI
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicColorRGBA
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicFont
from ...sockets import NodeSocketLogicImage
from ...sockets import NodeSocketLogicList
from ...enum_types import _writeable_widget_attrs
from ...name_maps import _ui_widget_attributes
from bpy.props import EnumProperty


@node_type
class LogicNodeGetUIWidgetAttr(LogicNodeParameterType):
    bl_idname = "LogicNodeGetUIWidgetAttr"
    bl_label = "Get Widget Attribute"
    bl_description = 'UI Widget attribute'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetUIWidgetAttr"

    def update_draw(self, context=None):
        if not self.ready:
            return
        attr = self.widget_attr
        self.outputs[0].enabled = attr in ['show', 'use_clipping', 'wrap', 'shadow']
        self.outputs[1].enabled = attr in ['bg_color', 'border_color', 'shadow_color', 'font_color', 'hover_color']
        self.outputs[2].enabled = attr in ['opacity', 'font_opacity']
        self.outputs[3].enabled = attr in ['pos', 'pivot', 'size', 'shadow_offset']
        self.outputs[4].enabled = attr in ['halign', 'valign', 'text', 'text_halign', 'text_valign', 'orientation']
        self.outputs[5].enabled = attr in ['spacing', 'font_size', 'icon', 'rows', 'cols', 'border_width']
        self.outputs[6].enabled = attr in ['width', 'height', 'line_height', 'angle', 'radius', 'starting_angle']
        self.outputs[7].enabled = attr in ['font']
        self.outputs[8].enabled = attr in ['texture']
        self.outputs[9].enabled = attr in ['points']
        for socket in self.outputs:
            socket.name = _ui_widget_attributes.get(attr)

    widget_attr: EnumProperty(
        items=_writeable_widget_attrs,
        name='',
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicUI, "Widget", 'widget')
        self.add_output(NodeSocketLogicBoolean, "Visibility", 'BOOL')
        self.add_output(NodeSocketLogicColorRGBA, "", 'COLOR', {'enabled': False})
        self.add_output(NodeSocketLogicFloatFactor, "", 'ALPHA', {'enabled': False})
        self.add_output(NodeSocketLogicVectorXY, "", 'VEC2', {'enabled': False})
        self.add_output(NodeSocketLogicString, "", 'STR', {'enabled': False})
        self.add_output(NodeSocketLogicInteger, "", 'INT', {'enabled': False})
        self.add_output(NodeSocketLogicFloat, "", 'FLOAT', {'enabled': False})
        self.add_output(NodeSocketLogicFont, "", 'FONT', {'enabled': False})
        self.add_output(NodeSocketLogicImage, "", 'IMG', {'enabled': False})
        self.add_output(NodeSocketLogicList, "", 'POINTS', {'enabled': False})
        LogicNodeParameterType.init(self, context)

    def get_attributes(self):
        return [("widget_attr", repr(self.widget_attr))]

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'widget_attr', text='')

    # XXX Remove for 5.0
    def get_input_names(self):
        return ['widget']

    # XXX Remove for 5.0
    def get_output_names(self):
        return ['BOOL', 'COLOR', 'ALPHA', 'VEC2', 'STR', 'INT', 'FLOAT', 'FONT', 'IMG']
