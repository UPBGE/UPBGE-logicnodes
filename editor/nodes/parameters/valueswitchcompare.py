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
    bl_description = 'Choose between multiple values depending on an input value'
    bl_width_min = 100
    bl_width_default = 172
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULValueSwitchListCompare"

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
        self.add_input(NodeSocketLogicValue, "Switch:", 'p0')
        self.add_input(NodeSocketLogicValue, "Default", 'val_default')
        self.add_input(NodeSocketLogicValue, "Case A", 'pa')
        self.add_input(NodeSocketLogicValue, "", 'val_a')
        self.add_input(NodeSocketLogicValue, "Case B", 'pb')
        self.add_input(NodeSocketLogicValue, "", 'val_b')
        self.add_input(NodeSocketLogicValue, "Case C", 'pc')
        self.add_input(NodeSocketLogicValue, "", 'val_c')
        self.add_input(NodeSocketLogicValue, "Case D", 'pd')
        self.add_input(NodeSocketLogicValue, "", 'val_d')
        self.add_input(NodeSocketLogicValue, "Case E", 'pe')
        self.add_input(NodeSocketLogicValue, "", 'val_e')
        self.add_input(NodeSocketLogicValue, "Case F", 'pf')
        self.add_input(NodeSocketLogicValue, "", 'val_f')
        self.add_output(NodeSocketLogicParameter, "Result", 'RESULT')
        LogicNodeParameterType.init(self, context)
        self.hide = True

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

    # XXX: Remove for 5.0
    def get_attributes(self):
        return [
            ("operator", f'{self.operator}'),
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['RESULT']
