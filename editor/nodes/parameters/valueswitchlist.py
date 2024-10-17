from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeValueSwitchList(LogicNodeParameterType):
    bl_idname = "NLValueSwitchList"
    bl_label = "Value Switch List"
    bl_description = 'Choose between multiple values depending on an input value'
    bl_width_min = 100
    bl_width_default = 160
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULValueSwitchList"

    def init(self, context):
        self.add_input(NodeSocketLogicBoolean, "if A", 'ca')
        self.add_input(NodeSocketLogicValue, "", 'val_a')
        self.add_input(NodeSocketLogicBoolean, "elif B", 'cb')
        self.add_input(NodeSocketLogicValue, "", 'val_b')
        self.add_input(NodeSocketLogicBoolean, "elif C", 'cc')
        self.add_input(NodeSocketLogicValue, "", 'val_c')
        self.add_input(NodeSocketLogicBoolean, "elif D", 'cd')
        self.add_input(NodeSocketLogicValue, "", 'val_d')
        self.add_input(NodeSocketLogicBoolean, "elif E", 'ce')
        self.add_input(NodeSocketLogicValue, "", 'val_e')
        self.add_input(NodeSocketLogicBoolean, "elif F", 'cf')
        self.add_input(NodeSocketLogicValue, "", 'val_f')
        self.add_output(NodeSocketLogicParameter, "Result", 'VAL')
        LogicNodeParameterType.init(self, context)
        self.hide = True

    def update_draw(self, context=None):
        for x in range(0, 10, 2):
            if self.inputs[x].is_linked or self.inputs[x].default_value == True:
                self.inputs[x].enabled = True
                self.inputs[x+1].enabled = True
                self.inputs[x+2].enabled = True
            elif not self.inputs[x+1].is_linked:
                self.inputs[x+1].enabled = False
                self.inputs[x+2].enabled = False

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "ca", 'val_a',
            "cb", 'val_b',
            "cc", 'val_c',
            "cd", 'val_d',
            "ce", 'val_e',
            "cf", 'val_f'
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['VAL']
