from bpy.types import NodeLink
from ..node import node_type
from ..node import LogicNodeUIType
from ..node import WIDGETS
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloatAngle
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicColorRGBA
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicUI
from ...enum_types import _ui_layout_types
from ...enum_types import _ui_boxlayout_types
from ...enum_types import _ui_halign_types
from ...enum_types import _ui_valign_types
from bpy.props import EnumProperty
from bpy.props import BoolProperty
from mathutils import Vector
import math


@node_type
class LogicNodeCreateUILayout(LogicNodeUIType):
    bl_idname = "LogicNodeCreateUILayout"
    bl_label = "Create Layout"
    bl_description = 'Create a new layout. A layout allows you to attach and arrange other widgets'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULCreateUILayout"

    def update_draw(self, context=None):
        self.inputs[4].enabled = self.layout_type != 'PolarLayout'
        self.inputs[5].enabled = self.layout_type != 'PolarLayout'
        self.inputs[7].enabled = self.layout_type != 'PolarLayout'
        self.inputs[8].enabled = self.layout_type != 'PolarLayout'
        self.inputs[9].enabled = self.layout_type != 'PolarLayout'
        self.inputs[10].enabled = (self.layout_type == 'BoxLayout')
        if len(self.inputs) > 11:  # XXX: Remove check for 4.0
            self.inputs[11].enabled = (self.layout_type == 'GridLayout')
            self.inputs[12].enabled = (self.layout_type == 'GridLayout')
            self.inputs[13].enabled = (self.layout_type == 'GridLayout')
            self.inputs[14].enabled = (self.layout_type == 'PolarLayout')
            self.inputs[15].enabled = (self.layout_type == 'PolarLayout')
        
        w = WIDGETS.get(self, None)
        if w is None:
            return
        if w.__class__ is not self.get_ui_class():
            parent = w.parent
            w.remove()
            del WIDGETS[self]
            w = WIDGETS[self] = self.get_ui_class()()
            w.update = self.update_widget
            parent.add_widget(w)

    def update_widget(self):
        from uplogic.ui.preview.layout import BoxLayout, GridLayout, ArrangedLayout, PolarLayout
        w = WIDGETS.get(self, None)
        ipts = self.inputs
        if w is None:
            return
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
        w.border_width = ipts[8].default_value
        w.border_color = Vector(ipts[9].default_value)
        ipts[10].enabled = False
        is_box = isinstance(w, BoxLayout)
        is_grid = isinstance(w, GridLayout)
        if is_box or is_grid:
            w.spacing = ipts[11].default_value
            w.orientation = self.boxlayout_type
            if is_grid:
                w.rows = ipts[12].default_value
                w.cols = ipts[13].default_value
        if isinstance(w, PolarLayout):
            w.starting_angle = math.degrees(ipts[14].default_value)
            w.radius = ipts[15].default_value
        if isinstance(w, ArrangedLayout):
            ipts[10].enabled = True
            w.arrange()

    layout_type: EnumProperty(items=_ui_layout_types, name='Layout Type', update=update_draw)
    boxlayout_type: EnumProperty(items=_ui_boxlayout_types, name='Orientation')
    halign_type: EnumProperty(items=_ui_halign_types, name='X')
    valign_type: EnumProperty(items=_ui_valign_types, name='Y')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicUI, "Parent", 'parent')
        self.add_input(NodeSocketLogicBoolean, "Relative Position", 'rel_pos')
        self.add_input(NodeSocketLogicVectorXY, "", 'pos')
        self.add_input(NodeSocketLogicBoolean, "Relative Size", 'rel_size')
        self.add_input(NodeSocketLogicVectorXY, "", 'size', {'default_value': (100., 100.)})
        self.add_input(NodeSocketLogicFloatAngle, "Angle", 'angle')
        self.add_input(NodeSocketLogicColorRGBA, "Color", 'color', {'default_value': (0, 0, 0, 0)})
        self.add_input(NodeSocketLogicIntegerPositive, "Border Width", 'border_width', {'default_value': 1})
        self.add_input(NodeSocketLogicColorRGBA, "Border Color", 'border_color', {'default_value': (0, 0, 0, 0)})
        self.add_input(NodeSocketLogicBoolean, "Inverted", 'inverted')
        self.add_input(NodeSocketLogicInteger, "Spacing", 'spacing')
        self.add_input(NodeSocketLogicInteger, "Rows", 'rows')
        self.add_input(NodeSocketLogicInteger, "Columns", 'cols')
        self.add_input(NodeSocketLogicFloatAngle, "Starting Angle", 'starting_angle')
        self.add_input(NodeSocketLogicFloat, "Radius", 'radius')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        self.add_output(NodeSocketLogicUI, "Layout", 'WIDGET')
        LogicNodeUIType.init(self, context)

    def get_ui_class(self):
        from uplogic.ui.preview.layout import BoxLayout, GridLayout, FloatLayout, RelativeLayout, PolarLayout
        return {
            'FloatLayout': FloatLayout,
            'RelativeLayout': RelativeLayout,
            'BoxLayout': BoxLayout,
            'GridLayout': GridLayout,
            'PolarLayout': PolarLayout
        }.get(self.layout_type)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'preview')
        layout.prop(self, 'layout_type', text='')
        if self.layout_type in ['BoxLayout', 'GridLayout']:
            layout.prop(self, 'boxlayout_type', text='')
        layout.prop(self, 'halign_type', text='X')
        layout.prop(self, 'valign_type', text='Y')

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", 'WIDGET']

    def get_attributes(self):
        return [
            ("layout_type", repr(self.layout_type)),
            ("boxlayout_type", repr(self.boxlayout_type)),
            ("halign_type", repr(self.halign_type)),
            ("valign_type", repr(self.valign_type))
        ]

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
            "border_width",
            "border_color",
            "inverted",
            'spacing',
            "rows",
            "columns",
            "starting_angle",
            "radius",
        ]
