from ...enum_types import _enum_logic_operators
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicFloatPositive
from ..node import LogicNodeConditionType
from ..node import node_type
from bpy.props import EnumProperty


@node_type
class LogicNodeCompare(LogicNodeConditionType):
    bl_idname = "NLConditionLogicOperation"
    bl_label = "Compare"
    nl_category = "Math"
    nl_module = "conditions"

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.inputs[2].enabled = False

    operator: EnumProperty(
        name='Operator',
        items=_enum_logic_operators,
        update=update_draw
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text='')

    def init(self, context):
        self.add_input(NodeSocketLogicValue, "", {'value_type': 'FLOAT'})
        self.add_input(NodeSocketLogicValue, "", {'value_type': 'FLOAT'})
        self.add_input(NodeSocketLogicFloatPositive, "Threshold", {'enabled': False})
        self.add_output(NodeSocketLogicCondition, "Result")
        LogicNodeConditionType.init(self, context)

    nl_class = "ULCompare"

    def get_input_names(self):
        return ["param_a", "param_b", 'threshold']

    def get_attributes(self):
        return [("operator", f'{self.operator}')]

    def get_output_names(self):
        return ['RESULT']
