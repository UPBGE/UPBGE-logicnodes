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
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    nl_module = 'actions'
    nl_class = "ULGamepadLook"

    def update_draw(self, context=None):
        if not self.ready:
            return
        ipts = self.inputs
        ipts[8].enabled = ipts[7].value
        ipts[10].enabled = ipts[9].value

    axis: EnumProperty(
        name='Axis',
        items=_enum_controller_stick_operators,
        description="Gamepad Sticks",
        update=update_draw
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicObject, 'Main Object')
        self.add_input(NodeSocketLogicObject, 'Head Object (Optional)')
        self.add_input(NodeSocketLogicInvertXY, 'Inverted', {'x': True})
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Index')
        self.add_input(NodeSocketLogicFloatPositive, 'Sensitivity', {'value': .25})
        self.add_input(NodeSocketLogicFloatPositive, 'Exponent', {'value': 2.3})
        self.add_input(NodeSocketLogicBoolean, 'Cap Left / Right')
        self.add_input(NodeSocketLogicVectorXYAngle, '')
        self.add_input(NodeSocketLogicBoolean, 'Cap Up / Down')
        self.add_input(NodeSocketLogicVectorXYAngle, '', {'value_x': radians(89), 'value_y': -radians(89)})
        self.add_input(NodeSocketLogicFloatPositive, 'Threshold', {'value': .1})
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "axis", text='')

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

    def get_output_names(self):
        return ["DONE"]

    def get_attributes(self):
        return [("axis", f'{self.axis}')]
