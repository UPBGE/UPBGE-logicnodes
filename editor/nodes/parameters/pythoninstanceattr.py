from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodePythonInstanceAttr(LogicNodeParameterType):
    bl_idname = "NLParameterGetAttribute"
    bl_label = "Get Instance Attribute"
    bl_description = 'An attribute from a python object'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetPyInstanceAttr"

    def init(self, context):
        self.add_input(NodeSocketLogicPython, 'Instance', 'instance')
        self.add_input(NodeSocketLogicString, 'Attribute', 'attr')
        self.add_output(NodeSocketLogicParameter, 'Value', 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['instance', 'attr']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
