from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicIntegerPositiveCent
from ...sockets import NodeSocketLogicCondition
from ...enum_types import _enum_controller_buttons_operators
from bpy.props import EnumProperty
from bpy.props import BoolProperty


@node_type
class LogicNodeGamepadButtonUp(LogicNodeConditionType):
    bl_idname = "NLGamepadButtonUpCondition"
    bl_label = "Button Up"
    nl_module = 'uplogic.nodes.conditions'
    deprecated = True

    button: EnumProperty(
        name='Button',
        items=_enum_controller_buttons_operators,
        description="Controller Buttons"
    )
    pulse: BoolProperty(
        description=(
            'ON: True until the button is released, '
            'OFF: True when pressed, then False until pressed again'
        )
    )

    def init(self, context):
        self.add_input(NodeSocketLogicIntegerPositiveCent, 'Index')
        self.add_output(NodeSocketLogicCondition, "Released")
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "pulse", text="Each Frame")
        layout.prop(self, "button", text='')

    nl_class = "ULGamepadButtonUp"

    def get_input_names(self):
        return ["index"]

    def get_output_names(self):
        return ["BUTTON"]

    def get_attributes(self):
        return [
            ("pulse", self.pulse),
            ("button", self.button)
        ]
