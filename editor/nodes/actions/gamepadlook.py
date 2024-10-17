from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicInvertXY
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXYAngle
from ...enum_types import _enum_controller_stick_operators
from bpy.props import EnumProperty
from math import radians


@node_type
class LogicNodeGamepadLook(LogicNodeActionType):
    bl_idname = "NLGamepadLook"
    bl_label = "Gamepad Look"
    bl_description = 'Map gamepad input to look behavior'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULGamepadLook"

    def update_draw(self, context=None):
        if not self.ready:
            return
        ipts = self.inputs
        ipts[8].enabled = ipts[7].default_value
        ipts[10].enabled = ipts[9].default_value

    axis: EnumProperty(
        name='Axis',
        items=_enum_controller_stick_operators,
        description="Gamepad Sticks",
        update=update_draw,
        default='1'
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicObject, 'Body', 'main_obj')
        self.add_input(NodeSocketLogicObject, 'Head', 'head_obj')
        self.add_input(NodeSocketLogicInvertXY, 'Inverted', 'inverted')
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Index', 'index')
        self.add_input(NodeSocketLogicFloatPositive, 'Sensitivity', 'sensitivity', {'default_value': .25})
        self.add_input(NodeSocketLogicFloatPositive, 'Exponent', 'exponent', {'default_value': 2.3})
        self.add_input(NodeSocketLogicBoolean, 'Cap Left / Right', 'use_cap_x')
        self.add_input(NodeSocketLogicVectorXYAngle, '', 'cap_x')
        self.add_input(NodeSocketLogicBoolean, 'Cap Up / Down', 'use_cap_y')
        self.add_input(NodeSocketLogicVectorXYAngle, '', 'cap_y', {'default_value': (-radians(89), radians(89))})
        self.add_input(NodeSocketLogicFloatPositive, 'Threshold', 'threshold', {'default_value': .1})
        self.add_output(NodeSocketLogicCondition, "Done", 'DONE')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "axis", text='')

    def get_attributes(self):
        return [("axis", f'{self.axis}')]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            'condition',
            'main_obj',
            'head_obj',
            'inverted',
            "index",
            'sensitivity',
            'exponent',
            'use_cap_x',
            'cap_x',
            'use_cap_y',
            'cap_y',
            'threshold'
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["DONE"]
