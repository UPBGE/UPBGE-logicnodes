from ...enum_types import _enum_logic_operators
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicFloatPositive
from ..node import LogicNodeConditionType
from ..node import node_type
from bpy.props import EnumProperty


@node_type
class LogicNodeCompare(LogicNodeConditionType):
    bl_idname = "NLConditionLogicOperation"
    bl_label = 'Compare'
    bl_description = 'Compare a value to another'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = 'ULCompare'

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
        self.add_input(NodeSocketLogicValue, "", 'param_a', {'value_type': 'FLOAT'})
        self.add_input(NodeSocketLogicValue, "", 'param_b', {'value_type': 'FLOAT'})
        self.add_input(NodeSocketLogicFloatPositive, "Threshold", 'threshold', {'enabled': False})
        self.add_output(NodeSocketLogicBoolean, "Result", 'RESULT')
        LogicNodeConditionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["param_a", "param_b", 'threshold']

    def get_attributes(self):
        return [("operator", f'{self.operator}')]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['RESULT']
