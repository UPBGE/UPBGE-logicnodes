from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicInvertXY
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXYAngle
from ...sockets import NodeSocketLogicFloatFactor
from ...enum_types import _enum_look_axis
from bpy.props import EnumProperty
from bpy.props import BoolProperty
from math import radians


@node_type
class LogicNodeMouseLook(LogicNodeActionType):
    bl_idname = "NLActionMouseLookNode"
    bl_label = "Mouse Look"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULMouseLook"

    def update_draw(self, context=None):
        if len(self.inputs) < 10:
            return
        if self.inputs[5].default_value:
            self.inputs[6].enabled = True
        else:
            self.inputs[6].enabled = False
        if self.inputs[7].default_value:
            self.inputs[8].enabled = True
        else:
            self.inputs[8].enabled = False

    axis: EnumProperty(
        name='Axis',
        items=_enum_look_axis,
        update=update_draw,
        default="1"
    )

    center_mouse: BoolProperty(
        name='Center Mouse',
        default=True
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Body")
        self.add_input(NodeSocketLogicObject, "Head")
        self.add_input(NodeSocketLogicInvertXY, "")
        self.add_input(NodeSocketLogicFloat, "Sensitivity", None, {'default_value': 1.0})
        self.add_input(NodeSocketLogicBoolean, "Cap Left / Right")
        self.add_input(NodeSocketLogicVectorXYAngle, "")
        self.add_input(NodeSocketLogicBoolean, "Cap Up / Down")
        self.add_input(NodeSocketLogicVectorXYAngle, "", None, {'default_value': (radians(-89), radians(89))})
        self.add_input(NodeSocketLogicFloatFactor, "Smoothing")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        r = layout.row(align=True)
        r.label(text="Front:")
        r.prop(self, "axis", text="")
        layout.prop(self, "center_mouse")

    def get_output_names(self):
        return ["OUT"]

    def get_attributes(self):
        return [
            ("axis", self.axis),
            ("center_mouse", self.center_mouse)
        ]

    def get_input_names(self):
        return [
            "condition",
            "game_object_x",
            "game_object_y",
            "inverted",
            "sensitivity",
            "use_cap_z",
            "cap_z",
            "use_cap_y",
            "cap_y",
            'smooth'
        ]
