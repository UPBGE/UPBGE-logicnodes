from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicCondition
from ...enum_types import _enum_controller_buttons_operators
from ...enum_types import _enum_input_types
from bpy.props import EnumProperty


@node_type
class LogicNodeGamepadButton(LogicNodeConditionType):
    bl_idname = "NLGamepadButtonsCondition"
    bl_label = "Button"
    nl_category = "Input"
    nl_subcat = 'Gamepad'
    nl_module = 'conditions'

    button: EnumProperty(
        name='Button',
        items=_enum_controller_buttons_operators,
        description="Controller Buttons",
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
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Index')
        self.add_output(NodeSocketLogicCondition, "Pressed")
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "button", text='')
        layout.prop(self, "input_type", text='')

    nl_class = "ULGamepadButton"

    def get_input_names(self):
        return ["index"]

    def get_output_names(self):
        return ["BUTTON"]

    def get_attributes(self):
        return [
            ("button", self.button),
            ("input_type", self.input_type)
        ]
