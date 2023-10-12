from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloatAngle
from ...sockets import NodeSocketLogicUI
from ...sockets import NodeSocketLogicImage
from ...enum_types import _ui_halign_types
from ...enum_types import _ui_valign_types
from bpy.props import EnumProperty


@node_type
class LogicNodeCreateUIImage(LogicNodeActionType):
    bl_idname = "LogicNodeCreateUIImage"
    bl_label = "Create Image"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULCreateUIImage"

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
        self.add_input(NodeSocketLogicImage, "")
        self.add_output(NodeSocketLogicCondition, "Done")
        self.add_output(NodeSocketLogicUI, "Label")
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')

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
            "rel_size",
            "size",
            "angle",
            "texture"
        ]
