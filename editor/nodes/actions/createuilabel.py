from ..node import WIDGETS, node_type
from ..node import LogicNodeUIType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloatAngle
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicColorRGBA
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicUI
from ...sockets import NodeSocketLogicFont
from ...sockets import NodeSocketLogicString
from ...enum_types import _ui_halign_types
from ...enum_types import _ui_valign_types
from bpy.props import EnumProperty
import math


@node_type
class LogicNodeCreateUILabel(LogicNodeUIType):
    bl_idname = "LogicNodeCreateUILabel"
    bl_label = "Create Label"
    bl_description = 'Create a new widget to show text'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULCreateUILabel"

    halign_type: EnumProperty(items=_ui_halign_types, name='X')
    valign_type: EnumProperty(items=_ui_valign_types, name='Y')

    def get_ui_class(self):
        from uplogic.ui.preview.label import Label
        return Label

    def update_widget(self):
        w = WIDGETS.get(self, None)
        if w is None:
            return
        ipts = self.inputs
        w.relative = {'pos': ipts[2].default_value}
        w.pos = ipts[3].default_value
        w.angle = math.degrees(ipts[4].default_value)
        w.text = ipts[5].default_value
        w.font = ipts[6].default_value
        w.font_size = ipts[7].default_value
        w.line_height = ipts[8].default_value
        w.font_color = ipts[9].default_value
        w.shadow = ipts[10].default_value
        w.shadow_offset = ipts[11].default_value
        w.shadow_color = ipts[12].default_value
        w.halign = self.halign_type
        w.valign = self.valign_type

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicUI, "Parent", 'parent')
        self.add_input(NodeSocketLogicBoolean, "Relative Position", 'rel_pos')
        self.add_input(NodeSocketLogicVectorXY, "", 'pos')
        self.add_input(NodeSocketLogicFloatAngle, "Angle", 'angle')
        self.add_input(NodeSocketLogicString, "Text", 'text')
        self.add_input(NodeSocketLogicFont, "", 'font')
        self.add_input(NodeSocketLogicInteger, "Font Size", 'font_size', {'default_value': 12})
        self.add_input(NodeSocketLogicFloat, "Line Height", 'line_height', {'default_value': 1.5})
        self.add_input(NodeSocketLogicColorRGBA, "Font Color", 'font_color', {'default_value': (1, 1, 1, 1)})
        self.add_input(NodeSocketLogicBoolean, "Use Shadow", 'use_shadow')
        self.add_input(NodeSocketLogicVectorXY, "Shadow Offset", 'shadow_offset', {'default_value': (1., -1.)})
        self.add_input(NodeSocketLogicColorRGBA, "Shadow Color", 'shadow_color', {'default_value': (0, 0, 0, .5)})
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        self.add_output(NodeSocketLogicUI, "Label", 'WIDGET')
        LogicNodeUIType.init(self, context)

    def update_draw(self, context=None):
        if len(self.inputs) < 13:
            return
        shadow = self.inputs[10].default_value
        self.inputs[11].enabled = shadow
        self.inputs[12].enabled = shadow

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')

    def get_attributes(self):
        return [
            ("halign_type", repr(self.halign_type)),
            ("valign_type", repr(self.valign_type))
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", 'WIDGET']

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            'parent',
            'rel_pos',
            "pos",
            "angle",
            "text",
            "font",
            "font_size",
            "line_height",
            "font_color",
            "use_shadow",
            "shadow_offset",
            "shadow_color",
        ]
