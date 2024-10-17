from ..node import node_type
from ..node import LogicNodeConditionType
from ...sockets import NodeSocketLogicMouseButton
from ...sockets import NodeSocketLogicCondition
from ...enum_types import _enum_input_types
from bpy.props import EnumProperty


@node_type
class LogicNodeMouseButton(LogicNodeConditionType):
    bl_idname = "NLMousePressedCondition"
    bl_label = "Mouse Button"
    bl_description = 'Register mouse button activity'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULMousePressed"

    input_type: EnumProperty(
        name='Input Type',
        items=_enum_input_types,
        description="Type of input recognition"
    )

    search_tags = [
        ['Mouse Button', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicMouseButton, "", 'mouse_button_code')
        self.add_output(NodeSocketLogicCondition, "If Pressed", 'OUT')
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'input_type', text='')

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["mouse_button_code"]

    def get_attributes(self):
        return [("input_type", self.input_type)]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
