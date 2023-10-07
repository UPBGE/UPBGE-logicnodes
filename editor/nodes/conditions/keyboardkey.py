from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicKeyboardKey
from ...sockets import NodeSocketLogicCondition
from ...enum_types import _enum_input_types
from bpy.props import EnumProperty


@node_type
class LogicNodeKeyboardKey(LogicNodeConditionType):
    bl_idname = "NLKeyPressedCondition"
    bl_label = "Key"
    nl_module = 'conditions'

    input_type: EnumProperty(
        name='Input Type',
        items=_enum_input_types,
        description="Type of input recognition"
    )

    def init(self, context):
        self.add_input(NodeSocketLogicKeyboardKey, "")
        self.add_output(NodeSocketLogicCondition, "If Pressed")
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'input_type', text='')

    nl_class = "ULKeyPressed"

    def get_input_names(self):
        return ["key_code"]

    def get_attributes(self):
        return [("input_type", self.input_type)]

    def get_output_names(self):
        return ['OUT']
