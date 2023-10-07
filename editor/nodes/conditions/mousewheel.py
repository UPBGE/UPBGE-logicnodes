from ...enum_types import _enum_mouse_wheel_direction
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicInteger
from ..node import LogicNodeConditionType
from ..node import node_type
from bpy.props import EnumProperty


@node_type
class LogicNodeMouseWheel(LogicNodeConditionType):
    bl_idname = "NLConditionMouseWheelMoved"
    bl_label = "Wheel"
    nl_module = 'conditions'
    deprecated = True

    wheel_direction: EnumProperty(items=_enum_mouse_wheel_direction, default='3')

    def init(self, context):
        self.add_input(NodeSocketLogicParameter, '', {'enabled': False})
        self.add_output(NodeSocketLogicCondition, "When Scrolled")
        self.add_output(NodeSocketLogicInteger, "Difference")
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'wheel_direction', text='')

    nl_class = "ULMouseScrolled"

    def get_input_names(self):
        return ['_old_direction']

    def get_output_names(self):
        return ['OUT', 'DIFF']

    def get_attributes(self):
        return [("wheel_direction", self.wheel_direction)]
