from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFloat
from ...enum_types import _enum_controller_buttons_operators
from ...enum_types import _enum_input_types
from bpy.props import EnumProperty


@node_type
class LogicNodeGamepadButton(LogicNodeConditionType):
    bl_idname = "NLGamepadButtonsCondition"
    bl_label = "Gamepad Button"
    bl_description = 'Register gamepad button activity'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULGamepadButton"

    def update_draw(self, context=None):
        self.outputs[1].enabled = int(self.button) > 14

    button: EnumProperty(
        name='Button',
        items=_enum_controller_buttons_operators,
        description="Controller Buttons",
        update=update_draw
    )

    input_type: EnumProperty(
        name='Input Type',
        items=_enum_input_types,
        description="Type of input recognition",
    )

    search_tags = [
        ['Gamepad Button', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Index', 'index')
        self.add_output(NodeSocketLogicCondition, "Pressed", 'BUTTON')
        self.add_output(NodeSocketLogicFloat, "Strength", 'BUTTON')
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "button", text='')
        layout.prop(self, "input_type", text='')

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["index"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["BUTTON", 'BUTTON']

    def get_attributes(self):
        return [
            ("button", self.button),
            ("input_type", self.input_type)
        ]
