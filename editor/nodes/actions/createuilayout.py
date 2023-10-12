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
from ...enum_types import _ui_layout_types
from ...enum_types import _ui_boxlayout_types
from ...enum_types import _ui_halign_types
from ...enum_types import _ui_valign_types
from bpy.props import EnumProperty


@node_type
class LogicNodeCreateUILayout(LogicNodeActionType):
    bl_idname = "LogicNodeCreateUILayout"
    bl_label = "Create Layout"
    nl_module = 'uplogic.nodes.actions'

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.inputs[10].enabled = (self.layout_type == 'BoxLayout')

    layout_type: EnumProperty(items=_ui_layout_types, name='Layout Type', update=update_draw)
    boxlayout_type: EnumProperty(items=_ui_boxlayout_types, name='Orientation')
    halign_type: EnumProperty(items=_ui_halign_types, name='X')
    valign_type: EnumProperty(items=_ui_valign_types, name='Y')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicUI, "Parent")
        self.add_input(NodeSocketLogicBoolean, "Relative Position")
        self.add_input(NodeSocketLogicVectorXY, "")
        self.add_input(NodeSocketLogicBoolean, "Relative Size")
        self.add_input(NodeSocketLogicVectorXY, "", {'value_x': 100, 'value_y': 100})
        self.add_input(NodeSocketLogicFloatAngle, "Angle")
        self.add_input(NodeSocketLogicColorRGBA, "Color", {'value': [0, 0, 0, 0]})
        self.add_input(NodeSocketLogicIntegerPositive, "Border Width", {'value': 1})
        self.add_input(NodeSocketLogicColorRGBA, "Border Color", {'value': [0, 0, 0, 0]})
        self.add_input(NodeSocketLogicFloat, "Spacing")
        self.add_output(NodeSocketLogicCondition, "Done")
        self.add_output(NodeSocketLogicUI, "Layout")
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'layout_type', text='')
        if self.layout_type == 'BoxLayout':
            layout.prop(self, 'boxlayout_type', text='')
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')

    nl_class = "ULCreateUILayout"

    def get_output_names(self):
        return ["OUT", 'WIDGET']

    def get_attributes(self):
        return [
            ("layout_type", f'"{self.layout_type}"'),
            ("boxlayout_type", f'"{self.boxlayout_type}"'),
            ("halign_type", f'"{self.halign_type}"'),
            ("valign_type", f'"{self.valign_type}"')
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
            "border_width",
            "border_color",
            'spacing'
        ]
