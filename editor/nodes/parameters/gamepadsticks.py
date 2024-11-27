from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicInvertXY
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloat
from ...enum_types import _enum_controller_stick_operators
from bpy.props import EnumProperty


@node_type
class LogicNodeGamepadSticks(LogicNodeParameterType):
    bl_idname = "NLGamepadSticksCondition"
    bl_label = "Gamepad Sticks"
    bl_description = 'Stick input from an external controller'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGamepadSticks"

    axis: EnumProperty(
        name='Axis',
        items=_enum_controller_stick_operators,
        description="Gamepad Sticks"
    )

    def init(self, context):
        self.add_input(NodeSocketLogicInvertXY, 'Inverted', 'inverted')
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Index', 'index')
        self.add_input(NodeSocketLogicFloatPositive, 'Sensitivity', 'sensitivity', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloatFactor, 'Threshold', 'threshold', {'default_value': 0.1})
        self.add_output(NodeSocketLogicFloat, "X", 'X', {'enabled': False})
        self.add_output(NodeSocketLogicFloat, "Y", 'Y', {'enabled': False})
        self.add_output(NodeSocketLogicVectorXYZ, "Vector", 'VEC')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "axis", text='')

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['inverted', "index", 'sensitivity', 'threshold']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["X", "Y", "VEC"]

    def get_attributes(self):
        return [
            ("axis", f'{self.axis}')
        ]
