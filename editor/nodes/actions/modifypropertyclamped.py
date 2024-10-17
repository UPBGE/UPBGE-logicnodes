from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicGameProperty
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXY
from ...enum_types import _enum_object_property_types
from ...enum_types import _enum_math_operations
from bpy.props import EnumProperty


@node_type
class LogicNodeModifyPropertyClamped(LogicNodeActionType):
    bl_idname = "NLClampedModifyProperty"
    bl_label = "Clamped Modify Property"
    nl_module = 'uplogic.nodes.actions'
    deprecated = True
    deprecation_message = 'Replaced by "Modify Property" Node.'
    nl_class = "ULClampedModifyProperty"

    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default=0
    )

    operator: EnumProperty(
        name='Operation',
        items=_enum_math_operations
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicGameProperty, "Property", None, {'ref_index': 1})
        self.add_input(NodeSocketLogicFloat, "Value")
        self.add_input(NodeSocketLogicVectorXY, "Range")
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")
        layout.prop(self, "operator", text="")

    def get_attributes(self):
        return [
            ("mode", self.mode),
            ("operator", f'OPERATORS.get("{self.operator}")')
        ]

    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "property_name",
            "property_value",
            'range'
        ]

    def get_output_names(self):
        return ['OUT']
