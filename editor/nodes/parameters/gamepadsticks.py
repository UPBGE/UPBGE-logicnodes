from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloat
from ...enum_types import _enum_controller_stick_operators
from ....utilities import update_draw
from bpy.props import EnumProperty


@node_type
class LogicNodeGamepadSticks(LogicNodeParameterType):
    bl_idname = "NLGamepadSticksCondition"
    bl_label = "Sticks"
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    nl_module = 'parameters'

    axis: EnumProperty(
        name='Axis',
        items=_enum_controller_stick_operators,
        description="Gamepad Sticks",
        update=update_draw
    )

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicBoolean, 'Inverted')
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Index')
        self.add_input(NodeSocketLogicFloatPositive, 'Sensitivity', {'value': 1.0})
        self.add_input(NodeSocketLogicFloatPositive, 'Threshold', {'value': 0.05})
        self.add_output(NodeSocketLogicFloat, "X", {'enabled': False})
        self.add_output(NodeSocketLogicFloat, "Y", {'enabled': False})
        self.add_output(NodeSocketLogicVectorXYZ, "Vector")

    def draw_buttons(self, context, layout):
        layout.prop(self, "axis", text='')

    def get_netlogic_class_name(self):
        return "ULGamepadSticks"

    def get_input_names(self):
        return ['inverted', "index", 'sensitivity', 'threshold']

    def get_output_names(self):
        return ["X", "Y", "VEC"]

    def get_attributes(self):
        return [
            ("axis", f'{self.axis}')
        ]
