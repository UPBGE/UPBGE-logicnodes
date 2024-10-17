from ..node import node_type
from ..node import LogicNodeUIType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloatAngle
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicColorRGBA
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicUI
from ...sockets import NodeSocketLogicFont
from ...sockets import NodeSocketLogicString
from ...enum_types import _ui_halign_types
from ...enum_types import _ui_valign_types
from ..node import WIDGETS
from bpy.props import EnumProperty
import math
from mathutils import Vector




@node_type
class LogicNodeCreateUIButton(LogicNodeUIType):
    bl_idname = "LogicNodeCreateUIButton"
    bl_label = "Create Button"
    bl_description = 'Create a new interactible button widget'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULCreateUIButton"

    halign_type: EnumProperty(items=_ui_halign_types, name='X')
    valign_type: EnumProperty(items=_ui_valign_types, name='Y')
    text_halign_type: EnumProperty(items=_ui_halign_types, name='Text X', default='center')
    text_valign_type: EnumProperty(items=_ui_valign_types, name='Text Y', default='center')

    def get_ui_class(self):
        from uplogic.ui.preview.label import Label
        from uplogic.ui.preview.layout import RelativeLayout

        class PreviewButton(RelativeLayout):
            
            def __init__(self):
                super().__init__()
                self.label = Label(relative={'pos': True})
                self.add_widget(self.label)
        return PreviewButton

    def update_widget(self):
        w = WIDGETS.get(self, None)
        if w is None:
            return
        ipts = self.inputs
        w.relative = {
            'pos': ipts[2].default_value,
            'size': ipts[4].default_value
        }
        w.halign = self.halign_type
        w.valign = self.valign_type
        w.pos = ipts[3].default_value
        w.size = Vector(ipts[5].default_value)
        w.angle = math.degrees(ipts[6].default_value)
        w.bg_color = Vector(ipts[7].default_value)
        w.border_width = ipts[9].default_value
        w.border_color = Vector(ipts[10].default_value)
        
        w.label.text = ipts[11].default_value
        w.label.pos = Vector(ipts[12].default_value)
        w.label.font = ipts[13].default_value
        w.label.font_size = ipts[14].default_value
        w.label.line_height = ipts[15].default_value
        w.label.font_color = ipts[16].default_value
        # w.label.shadow = ipts[10].default_value
        # w.label.shadow_offset = ipts[11].default_value
        # w.label.shadow_color = ipts[12].default_value
        w.label.halign = self.text_halign_type
        w.label.valign = self.text_valign_type

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicUI, "Parent", 'parent')
        self.add_input(NodeSocketLogicBoolean, "Relative Position", 'rel_pos')
        self.add_input(NodeSocketLogicVectorXY, "", 'pos')
        self.add_input(NodeSocketLogicBoolean, "Relative Size", 'rel_size')
        self.add_input(NodeSocketLogicVectorXY, "", 'size', {'default_value': (100., 100.)})
        self.add_input(NodeSocketLogicFloatAngle, "Angle", 'angle')
        self.add_input(NodeSocketLogicColorRGBA, "Color", 'color', {'default_value': (0, 0, 0, 0)})
        self.add_input(NodeSocketLogicColorRGBA, "Hover Color", 'hover_color', {'default_value': (0, 0, 0, .5)})
        self.add_input(NodeSocketLogicIntegerPositive, "Border Width", 'border_width', {'default_value': 1})
        self.add_input(NodeSocketLogicColorRGBA, "Border Color", 'border_color', {'default_value': (0, 0, 0, 0)})
        self.add_input(NodeSocketLogicString, "Text", 'text')
        self.add_input(NodeSocketLogicVectorXY, "Text Position", 'text_pos', {'default_value': (.5, .5)})
        self.add_input(NodeSocketLogicFont, "Font", 'font')
        self.add_input(NodeSocketLogicIntegerPositive, "Font Size", 'font_size', {'default_value': 12})
        self.add_input(NodeSocketLogicFloat, "Line Height", 'line_height', {'default_value': 1.5})
        self.add_input(NodeSocketLogicColorRGBA, "Font Color", 'font_color', {'default_value': (1, 1, 1, 1)})
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        self.add_output(NodeSocketLogicUI, "Button", 'WIDGET')
        self.add_output(NodeSocketLogicCondition, "On Click", 'CLICK')
        self.add_output(NodeSocketLogicCondition, "On Hover", 'HOVER')
        self.add_output(NodeSocketLogicCondition, "On Release", 'RELEASE')
        LogicNodeUIType.init(self, context)

    def update_draw(self, context=None):
        if len(self.inputs) < 17:
            return
        has_text = True if self.inputs[11].default_value else False
        for ipt in [12, 13, 14, 15, 16]:
            self.inputs[ipt].enabled = has_text

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')
        if self.inputs[11].default_value:
            layout.prop(self, 'text_halign_type', text='Text X')
            layout.prop(self, 'text_valign_type', text='Text Y')

    def get_attributes(self):
        return [
            ("halign_type", repr(self.halign_type)),
            ("valign_type", repr(self.valign_type)),
            ("text_halign_type", repr(self.text_halign_type)),
            ("text_valign_type", repr(self.text_valign_type))
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", 'WIDGET', 'CLICK', 'HOVER', 'RELEASE']

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            'parent',
            'rel_pos',
            "pos",
            "rel_size",
            "size",
            "angle",
            "color",
            "hover_color",
            "border_width",
            "border_color",
            "text",
            "text_pos",
            "font",
            "font_size",
            "line_height",
            "font_color"
        ]


# @node_type
# class LogicNodeCreateButtonWidget(LogicNodeActionType):
#     bl_idname = "LogicNodeCreateButtonWidget"
#     bl_label = "Create Button"
#     nl_module = 'uplogic.nodes.actions'
#     nl_class = "ULCreateButtonWidget"

#     halign_type: EnumProperty(items=_ui_halign_types, name='X')
#     valign_type: EnumProperty(items=_ui_valign_types, name='Y')
#     text_halign_type: EnumProperty(items=_ui_halign_types, name='Text X', default='center')
#     text_valign_type: EnumProperty(items=_ui_valign_types, name='Text Y', default='center')

#     def init(self, context):
#         self.add_input(NodeSocketLogicCondition, "Condition")
#         self.add_input(NodeSocketLogicUI, "Parent")
#         self.add_input(NodeSocketLogicBoolean, "Relative Position")
#         self.add_input(NodeSocketLogicVectorXY, "")
#         self.add_input(NodeSocketLogicBoolean, "Relative Size")
#         self.add_input(NodeSocketLogicVectorXY, "", None, {'default_value': (100., 100.)})
#         self.add_input(NodeSocketLogicFloatAngle, "Angle")
#         self.add_input(NodeSocketLogicColorRGBA, "Color", None, {'default_value': (0, 0, 0, 0)})
#         self.add_input(NodeSocketLogicColorRGBA, "Hover Color", None, {'default_value': (0, 0, 0, .5)})
#         self.add_input(NodeSocketLogicIntegerPositive, "Border Width", None, {'default_value': 1})
#         self.add_input(NodeSocketLogicColorRGBA, "Border Color", None, {'default_value': (0, 0, 0, 0)})
#         self.add_input(NodeSocketLogicString, "Text")
#         self.add_input(NodeSocketLogicVectorXY, "Text Position", None, {'default_value': (.5, .5)})
#         self.add_input(NodeSocketLogicFont, "Font")
#         self.add_input(NodeSocketLogicIntegerPositive, "Font Size", None, {'default_value': 12})
#         self.add_input(NodeSocketLogicFloat, "Line Height", None, {'default_value': 1.5})
#         self.add_input(NodeSocketLogicColorRGBA, "Font Color", None, {'default_value': (1, 1, 1, 1)})
#         self.add_output(NodeSocketLogicCondition, "Done")
#         self.add_output(NodeSocketLogicUI, "Button")
#         self.add_output(NodeSocketLogicCondition, "On Click")
#         self.add_output(NodeSocketLogicCondition, "On Hover")
#         self.add_output(NodeSocketLogicCondition, "On Release")
#         LogicNodeActionType.init(self, context)

#     def update_draw(self, context=None):
#         if len(self.inputs) < 17:
#             return
#         has_text = True if self.inputs[11].default_value else False
#         for ipt in [12, 13, 14, 15, 16]:
#             self.inputs[ipt].enabled = has_text

#     def draw_buttons(self, context, layout) -> None:
#         layout.prop(self, 'halign_type', text='X')
#         layout.prop(self, 'valign_type', text='Y')
#         if self.inputs[11].default_value:
#             layout.prop(self, 'text_halign_type', text='Text X')
#             layout.prop(self, 'text_valign_type', text='Text Y')

#     def get_output_names(self):
#         return ["OUT", 'WIDGET', 'CLICK', 'HOVER', 'RELEASE']

#     def get_attributes(self):
#         return [
#             ("halign_type", repr(self.halign_type)),
#             ("valign_type", repr(self.valign_type)),
#             ("text_halign_type", repr(self.text_halign_type)),
#             ("text_valign_type", repr(self.text_valign_type))
#         ]

#     def get_input_names(self):
#         return [
#             "condition",
#             'parent',
#             'rel_pos',
#             "pos",
#             "rel_size",
#             "size",
#             "angle",
#             "color",
#             "hover_color",
#             "border_width",
#             "border_color",
#             "text",
#             "text_pos",
#             "font",
#             "font_size",
#             "line_height",
#             "font_color"
#         ]
