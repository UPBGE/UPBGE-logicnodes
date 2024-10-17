from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicFloatFactor
from ...enum_types import _enum_writable_member_names
from bpy.props import EnumProperty


@node_type
class LogicNodeSlowFollow(LogicNodeActionType):
    bl_idname = "NLSlowFollow"
    bl_label = "Slow Follow"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSlowFollow"
    bl_description = 'Linearly interpolate an attribute from one object to another'

    value_type: EnumProperty(
        name='Attribute',
        items=_enum_writable_member_names,
        default='worldPosition'
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicObject, "Target", 'target')
        self.add_input(NodeSocketLogicFloatFactor, "Factor", 'factor', {'default_value': 1})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "value_type", text='')

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "game_object", "target", "factor"]

    def get_attributes(self):
        return [
            ("value_type", repr(self.value_type)),
        ]
