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
from ...sockets import NodeSocketLogicFont
from ...sockets import NodeSocketLogicString
from ...enum_types import _ui_halign_types
from ...enum_types import _ui_valign_types
from bpy.props import EnumProperty


@node_type
class LogicNodeCreateUIButton(LogicNodeActionType):
    bl_idname = "LogicNodeCreateUIButton"
    bl_label = "Create Button"
    nl_category = "UI"
    nl_subcat = 'Widgets'
    nl_module = 'actions'
    halign_type: EnumProperty(items=_ui_halign_types, name='X')
    valign_type: EnumProperty(items=_ui_valign_types, name='Y')
    text_halign_type: EnumProperty(items=_ui_halign_types, name='Text X', default='center')
    text_valign_type: EnumProperty(items=_ui_valign_types, name='Text Y', default='center')

    def init(self, context):
        LogicNodeActionType.init(self, context)
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicUI, "Parent")
        self.add_input(NodeSocketLogicBoolean, "Relative Position")
        self.add_input(NodeSocketLogicVectorXY, "")
        self.add_input(NodeSocketLogicBoolean, "Relative Size")
        self.add_input(NodeSocketLogicVectorXY, "", {'value_x': 100, 'value_y': 100})
        self.add_input(NodeSocketLogicFloatAngle, "Angle")
        self.add_input(NodeSocketLogicColorRGBA, "Color", {'value': [0, 0, 0, 0]})
        self.add_input(NodeSocketLogicColorRGBA, "Hover Color", {'value': [0, 0, 0, .5]})
        self.add_input(NodeSocketLogicIntegerPositive, "Border Width", {'value': 1})
        self.add_input(NodeSocketLogicColorRGBA, "Border Color", {'value': [0, 0, 0, 0]})
        self.add_input(NodeSocketLogicString, "Text")
        self.add_input(NodeSocketLogicVectorXY, "Text Position", {'value_x': .5, 'value_y': .5})
        self.add_input(NodeSocketLogicFont, "Font")
        self.add_input(NodeSocketLogicIntegerPositive, "Font Size", {'value': 12})
        self.add_input(NodeSocketLogicFloat, "Line Height", {'value': 1.5})
        self.add_input(NodeSocketLogicColorRGBA, "Font Color", {'value': [1, 1, 1, 1]})
        self.add_output(NodeSocketLogicCondition, "Done")
        self.add_output(NodeSocketLogicUI, "Button")
        self.add_output(NodeSocketLogicCondition, "On Click")
        self.add_output(NodeSocketLogicCondition, "On Hover")
        self.add_output(NodeSocketLogicCondition, "On Release")
        self.update_draw()

    def update_draw(self):
        if len(self.inputs) < 17:
            return
        has_text = True if self.inputs[11].value else False
        for ipt in [12, 13, 14, 15, 16]:
            self.inputs[ipt].enabled = has_text

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')
        if self.inputs[11].value:
            layout.prop(self, 'text_halign_type', text='Text X')
            layout.prop(self, 'text_valign_type', text='Text Y')

    def get_netlogic_class_name(self):
        return "ULCreateUIButton"

    def get_output_names(self):
        return ["OUT", 'WIDGET', 'CLICK', 'HOVER', 'RELEASE']

    def get_attributes(self):
        return [
            ("halign_type", lambda: f'"{self.halign_type}"'),
            ("valign_type", lambda: f'"{self.valign_type}"'),
            ("text_halign_type", lambda: f'"{self.text_halign_type}"'),
            ("text_valign_type", lambda: f'"{self.text_valign_type}"')
        ]

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
