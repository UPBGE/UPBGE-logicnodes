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
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicObject, 'Body')
        self.add_input(NodeSocketLogicObject, 'Head')
        self.add_input(NodeSocketLogicInvertXY, 'Inverted')
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Index')
        self.add_input(NodeSocketLogicFloatPositive, 'Sensitivity', None, {'default_value': .25})
        self.add_input(NodeSocketLogicFloatPositive, 'Exponent', None, {'default_value': 2.3})
        self.add_input(NodeSocketLogicBoolean, 'Cap Left / Right')
        self.add_input(NodeSocketLogicVectorXYAngle, '')
        self.add_input(NodeSocketLogicBoolean, 'Cap Up / Down')
        self.add_input(NodeSocketLogicVectorXYAngle, '', None, {'default_value': (-radians(89), radians(89))})
        self.add_input(NodeSocketLogicFloatPositive, 'Threshold', None, {'default_value': .1})
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
