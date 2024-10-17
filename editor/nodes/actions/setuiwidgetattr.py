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
from ...sockets import NodeSocketLogicList
from ...enum_types import _writeable_widget_attrs
from bpy.props import EnumProperty


@node_type
class LogicNodeSetUIWidgetAttr(LogicNodeActionType):
    bl_idname = "LogicNodeSetUIWidgetAttr"
    bl_label = "Set Widget Attribute"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetUIWidgetAttr"
    bl_description = 'Set an attribute of a UI widget'

    def update_draw(self, context=None):
        if not self.ready:
            return
        attr = self.widget_attr
        self.inputs[2].enabled = attr in ['show', 'use_clipping', 'wrap', 'shadow']
        self.inputs[3].enabled = attr in ['bg_color', 'border_color', 'shadow_color', 'font_color', 'hover_color']
        self.inputs[4].enabled = attr in ['opacity', 'font_opacity']
        self.inputs[5].enabled = attr in ['pos', 'pivot', 'size', 'shadow_offset']
        self.inputs[6].enabled = attr in ['halign', 'valign', 'text', 'text_halign', 'text_valign', 'orientation']
        self.inputs[7].enabled = attr in ['spacing', 'font_size', 'icon', 'rows', 'cols', 'border_width']
        self.inputs[8].enabled = attr in ['width', 'height', 'line_height', 'radius']
        self.inputs[9].enabled = attr in ['font']
        self.inputs[10].enabled = attr in ['texture']
        self.inputs[11].enabled = attr in ['angle', 'starting_angle']
        self.inputs[12].enabled = attr in ['points']

    widget_attr: EnumProperty(items=_writeable_widget_attrs, name='', update=update_draw)

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicUI, "Widget", 'widget' )
        self.add_input(NodeSocketLogicBoolean, "", 'value')
        self.add_input(NodeSocketLogicColorRGBA, "", 'value', {'enabled': False})
        self.add_input(NodeSocketLogicFloatFactor, "", 'value', {'enabled': False})
        self.add_input(NodeSocketLogicVectorXY, "", 'value', {'enabled': False})
        self.add_input(NodeSocketLogicString, "", 'value', {'enabled': False})
        self.add_input(NodeSocketLogicInteger, "", 'value', {'enabled': False})
        self.add_input(NodeSocketLogicFloat, "", 'value', {'enabled': False})
        self.add_input(NodeSocketLogicFont, "", 'value', {'enabled': False})
        self.add_input(NodeSocketLogicImage, "", 'value', {'enabled': False})
        self.add_input(NodeSocketLogicFloatAngle, "", 'value', {'enabled': False})
        self.add_input(NodeSocketLogicList, "Points", 'value', {'enabled': False})
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        LogicNodeActionType.init(self, context)

    def get_attributes(self):
        return [("widget_attr", repr(self.widget_attr))]

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'widget_attr', text='')

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            'widget',
            'value',
            'value',
            'value',
            'value',
            'value',
            'value',
            'value',
            'value',
            'value',
            'value'
        ]
