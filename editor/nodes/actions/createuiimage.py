from ..node import node_type
from ..node import LogicNodeUIType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloatAngle
from ...sockets import NodeSocketLogicUI
from ...sockets import NodeSocketLogicImage
from ...enum_types import _ui_halign_types
from ...enum_types import _ui_valign_types
from bpy.props import EnumProperty
from bpy.props import BoolProperty
from ..node import WIDGETS
import math


@node_type
class LogicNodeCreateUIImage(LogicNodeUIType):
    bl_idname = "LogicNodeCreateUIImage"
    bl_label = "Create Image"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULCreateUIImage"
    bl_description = 'Create a new image widget'

    halign_type: EnumProperty(items=_ui_halign_types, name='X')
    valign_type: EnumProperty(items=_ui_valign_types, name='Y')
    aspect_ratio: BoolProperty(name='Use Aspect Ratio', default=True, description="Keep images' original width/height proportions")

    def get_ui_class(self):
        from uplogic.ui.preview.image import ImagePreview
        return ImagePreview

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
        w.size = ipts[5].default_value
        w.angle = math.degrees(ipts[6].default_value)
        if ipts[7].default_value:
            w.texture = ipts[7].default_value.name
        w.use_aspect_ratio = self.aspect_ratio

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicUI, "Parent", 'parent')
        self.add_input(NodeSocketLogicBoolean, "Relative Position", 'rel_pos')
        self.add_input(NodeSocketLogicVectorXY, "", 'pos')
        self.add_input(NodeSocketLogicBoolean, "Relative Size", 'rel_size')
        self.add_input(NodeSocketLogicVectorXY, "", 'size', {'default_value': (100., 100.)})
        self.add_input(NodeSocketLogicFloatAngle, "Angle", 'angle')
        self.add_input(NodeSocketLogicImage, "", 'texture')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        self.add_output(NodeSocketLogicUI, "Image", 'WIDGET')
        LogicNodeUIType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')
        layout.prop(self, 'aspect_ratio', text='Aspect Ratio')

    def get_attributes(self):
        return [
            ("halign_type", repr(self.halign_type)),
            ("valign_type", repr(self.valign_type)),
            ("aspect_ratio", self.aspect_ratio)
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
            "rel_size",
            "size",
            "angle",
            "texture"
        ]
