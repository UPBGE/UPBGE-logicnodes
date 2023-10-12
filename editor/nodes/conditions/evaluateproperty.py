from ...enum_types import _enum_logic_operators
from ...enum_types import _enum_object_property_types
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicGameProperty
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicValue
from ..node import LogicNodeConditionType
from ..node import node_type
from bpy.props import EnumProperty


@node_type
class LogicNodeEvaluateProperty(LogicNodeConditionType):
    bl_idname = "NLObjectPropertyOperator"
    bl_label = "Evaluate Property"
    nl_module = 'uplogic.nodes.conditions'

    mode: EnumProperty(
        name='Mode',
        items=_enum_object_property_types,
        default=0
    )

    operator: EnumProperty(
        name='Operator',
        items=_enum_logic_operators
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")
        layout.prop(self, "operator", text='')

    def init(self, context):
        self.add_input(NodeSocketLogicObject, 'Object')
        self.add_input(NodeSocketLogicGameProperty, "Property")
        self.add_input(NodeSocketLogicValue, '')
        self.add_output(NodeSocketLogicCondition, 'If True')
        self.add_output(NodeSocketLogicParameter, 'Value')
        LogicNodeConditionType.init(self, context)

    nl_class = "ULEvaluateProperty"

    def get_input_names(self):
        return [
            "game_object",
            "property_name",
            "compare_value"
        ]

    def get_attributes(self):
        return [
            ("mode", self.mode),
            ("operator", f'LOGIC_OPERATORS[{self.operator}]')
        ]

    def get_output_names(self):
        return ['OUT', "VAL"]
