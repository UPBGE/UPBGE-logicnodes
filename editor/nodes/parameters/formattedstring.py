from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeFormattedString(LogicNodeParameterType):
    bl_idname = "NLParameterFormattedString"
    bl_label = "Formatted String"
    nl_module = 'parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicString, "Format String", {'formatted': True, 'value': 'A is {} and B is {}'})
        self.add_input(NodeSocketLogicString, "A", {'value': 'Hello'})
        self.add_input(NodeSocketLogicString, "B", {'value': 'World'})
        self.add_input(NodeSocketLogicString, "C")
        self.add_input(NodeSocketLogicString, "D")
        self.add_output(NodeSocketLogicString, "String")
        LogicNodeParameterType.init(self, context)

    def update_draw(self, context=None):
        string = self.inputs[0].value
        count = string.count('{}')
        ipts = [1, 2, 3, 4]
        for ipt in ipts:
            if ipt <= count:
                self.inputs[ipt].enabled = True
            else:
                self.inputs[ipt].enabled = False

    def get_input_names(self):
        return ["format_string", "value_a", "value_b", "value_c", "value_d"]

    nl_class = "ULFormattedString"

    def get_output_names(self):
        return ["OUT"]
