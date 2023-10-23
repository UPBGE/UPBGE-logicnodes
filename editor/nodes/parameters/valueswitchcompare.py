from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicParameter
from ...enum_types import _enum_logic_operators
from bpy.props import EnumProperty


@node_type
class LogicNodeValueSwitchCompare(LogicNodeParameterType):
    bl_idname = "NLValueSwitchListCompare"
    bl_label = "Value Switch List Compare"
    bl_width_min = 100
    bl_width_default = 172
    nl_module = 'uplogic.nodes.parameters'

    def update_draw(self, context=None):
        if not self.ready:
            return
        for x in range(2, 12):
            if self.inputs[x].is_linked or self.inputs[x].default_value != "_None_":
                self.inputs[x].enabled = True
                self.inputs[x+1].enabled = True
                self.inputs[x+2].enabled = True
            elif not self.inputs[x+1].is_linked:
                self.inputs[x+1].enabled = False
                self.inputs[x+2].enabled = False

    operator: EnumProperty(
        name='Operator',
        items=_enum_logic_operators,
        update=update_draw
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator", text='')

    def init(self, context):
        self.add_input(NodeSocketLogicValue, "Switch:")
        self.add_input(NodeSocketLogicValue, "Default")
        self.add_input(NodeSocketLogicValue, "Case A")
        self.add_input(NodeSocketLogicValue, "")
        self.add_input(NodeSocketLogicValue, "Case B")
        self.add_input(NodeSocketLogicValue, "")
        self.add_input(NodeSocketLogicValue, "Case C")
        self.add_input(NodeSocketLogicValue, "")
        self.add_input(NodeSocketLogicValue, "Case D")
        self.add_input(NodeSocketLogicValue, "")
        self.add_input(NodeSocketLogicValue, "Case E")
        self.add_input(NodeSocketLogicValue, "")
        self.add_input(NodeSocketLogicValue, "Case F")
        self.add_input(NodeSocketLogicValue, "")
        self.add_output(NodeSocketLogicParameter, "Result")
        LogicNodeParameterType.init(self, context)
        self.hide = True

    nl_class = "ULValueSwitchListCompare"

    def get_input_names(self):
        return [
            "p0", "val_default",
            "pa", 'val_a',
            "pb", 'val_b',
            "pc", 'val_c',
            "pd", 'val_d',
            "pe", 'val_e',
            "pf", 'val_f'
        ]

    def get_attributes(self):
        return [
            ("operator", f'{self.operator}'),
        ]

    def get_output_names(self):
        return ['RESULT']
