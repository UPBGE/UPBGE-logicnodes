from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicLight
from ...sockets import NodeSocketLogicFloat
from ...enum_types import _enum_math_functions
from bpy.props import EnumProperty
from bpy.props import StringProperty


@node_type
class LogicNodeFormula(LogicNodeParameterType):
    bl_idname = "NLParameterMathFun"
    bl_label = "Formula"
    bl_description = 'Dynamic arithmetic operation'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULFormula"

    value: StringProperty(default='a + b', name='Formula')

    predefined_formulas: EnumProperty(
        name='Operation',
        items=_enum_math_functions,
        default="User Defined")

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "a", 'a')
        self.add_input(NodeSocketLogicFloat, "b", 'b')
        self.add_output(NodeSocketLogicFloat, "Result", 'OUT')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "predefined_formulas", text="Predef.")
        if self.predefined_formulas == 'User Defined':
            layout.prop(self, "value", text="Formula")

    def get_attributes(self):
        usr_def = 'User Defined'
        return [("formula", repr(self.value if self.predefined_formulas == usr_def else self.predefined_formulas))]

    # XXX Remove for 5.0
    def get_input_names(self):
        return ["a", "b"]

    # XXX Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
