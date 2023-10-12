from ..node import node_type
from ..node import LogicNodeActionType
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


@node_type
class LogicNodeCreateUILabel(LogicNodeActionType):
    bl_idname = "LogicNodeCreateUILabel"
    bl_label = "Create Label"
    nl_module = 'uplogic.nodes.actions'
    halign_type: EnumProperty(items=_ui_halign_types, name='X')
    valign_type: EnumProperty(items=_ui_valign_types, name='Y')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicUI, "Parent")
        self.add_input(NodeSocketLogicBoolean, "Relative Position")
        self.add_input(NodeSocketLogicVectorXY, "")
        self.add_input(NodeSocketLogicFloatAngle, "Angle")
        self.add_input(NodeSocketLogicString, "Text")
        self.add_input(NodeSocketLogicFont, "")
        self.add_input(NodeSocketLogicInteger, "Font Size", {'value': 12})
        self.add_input(NodeSocketLogicFloat, "Line Height", {'value': 1.5})
        self.add_input(NodeSocketLogicColorRGBA, "Font Color", {'value': [1, 1, 1, 1]})
        self.add_input(NodeSocketLogicBoolean, "Use Shadow")
        self.add_input(NodeSocketLogicVectorXY, "Shadow Offset", {'value_x': 1, 'value_y': -1})
        self.add_input(NodeSocketLogicColorRGBA, "Shadow Color", {'value': [0, 0, 0, .5]})
        self.add_output(NodeSocketLogicCondition, "Done")
        self.add_output(NodeSocketLogicUI, "Label")
        LogicNodeActionType.init(self, context)

    def update_draw(self, context=None):
        if len(self.inputs) < 13:
            return
        shadow = self.inputs[10].value
        self.inputs[11].enabled = shadow
        self.inputs[12].enabled = shadow

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')

    nl_class = "ULCreateUILabel"

    def get_output_names(self):
        return ["OUT", 'WIDGET']

    def get_attributes(self):
        return [
            ("halign_type", f'"{self.halign_type}"'),
            ("valign_type", f'"{self.valign_type}"')
        ]

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
