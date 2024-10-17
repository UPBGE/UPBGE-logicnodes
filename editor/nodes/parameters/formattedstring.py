from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeFormattedString(LogicNodeParameterType):
    bl_idname = "NLParameterFormattedString"
    bl_label = "Formatted String"
    bl_description = 'Dynamic string operation'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULFormattedString"

    def init(self, context):
        self.add_input(NodeSocketLogicString, "Format String", 'format_string', {'formatted': True, 'default_value': 'A is {} and B is {}'})
        self.add_input(NodeSocketLogicString, "A", 'value_a', {'default_value': 'Hello'})
        self.add_input(NodeSocketLogicString, "B", 'value_b', {'default_value': 'World'})
        self.add_input(NodeSocketLogicString, "C", 'value_c')
        self.add_input(NodeSocketLogicString, "D", 'value_d')
        self.add_output(NodeSocketLogicString, "String", 'OUT')
        LogicNodeParameterType.init(self, context)

    def update_draw(self, context=None):
        string = self.inputs[0].default_value
        count = string.count('{}')
        ipts = [1, 2, 3, 4]
        for ipt in ipts:
            if ipt <= count:
                self.inputs[ipt].enabled = True
            else:
                self.inputs[ipt].enabled = False

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["format_string", "value_a", "value_b", "value_c", "value_d"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
