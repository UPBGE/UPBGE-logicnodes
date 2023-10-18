from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodeValueSwitchList(LogicNodeParameterType):
    bl_idname = "NLValueSwitchList"
    bl_label = "Value Switch List"
    bl_width_min = 100
    bl_width_default = 160
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicBoolean, "if A")
        self.add_input(NodeSocketLogicValue, "")
        self.add_input(NodeSocketLogicBoolean, "elif B")
        self.add_input(NodeSocketLogicValue, "")
        self.add_input(NodeSocketLogicBoolean, "elif C")
        self.add_input(NodeSocketLogicValue, "")
        self.add_input(NodeSocketLogicBoolean, "elif D")
        self.add_input(NodeSocketLogicValue, "")
        self.add_input(NodeSocketLogicBoolean, "elif E")
        self.add_input(NodeSocketLogicValue, "")
        self.add_input(NodeSocketLogicBoolean, "elif F")
        self.add_input(NodeSocketLogicValue, "")
        self.add_output(NodeSocketLogicParameter, "Result")
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

    nl_class = "ULValueSwitchList"

    def get_input_names(self):
        return [
            "ca", 'val_a',
            "cb", 'val_b',
            "cc", 'val_c',
            "cd", 'val_d',
            "ce", 'val_e',
            "cf", 'val_f'
        ]

    def get_output_names(self):
        return ['VAL']
