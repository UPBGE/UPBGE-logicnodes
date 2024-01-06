from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicGameProperty
from ...sockets import NodeSocketLogicFloat
from ...enum_types import _enum_object_property_types
from ...enum_types import _enum_math_operations
from bpy.props import EnumProperty
from bpy.props import BoolProperty


@node_type
class LogicNodeModifyProperty(LogicNodeActionType):
    bl_idname = "NLAddToGameObjectGamePropertyActionNode"
    bl_label = "Modify Property"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULModifyProperty"

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.inputs[4].enabled = self.inputs[5].enabled = self.clamp
    clamp: BoolProperty(name='Clamp', update=update_draw)

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
        self.add_input(NodeSocketLogicFloat, "Min")
        self.add_input(NodeSocketLogicFloat, "Max", None, {'default_value': 1.0})
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")
        layout.prop(self, "operator", text="")
        layout.prop(self, "clamp", text="Clamp")


    def get_attributes(self):
        return [
            ('mode', self.mode),
            ('clamp', self.clamp),
            ("operator", f'OPERATORS.get("{self.operator}")')
        ]

    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "property_name",
            "property_value",
            'min_value',
            'max_value'
        ]

    def get_output_names(self):
        return ['OUT']
