from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicParameter


@node_type
class LogicNodePythonInstanceAttr(LogicNodeParameterType):
    bl_idname = "NLParameterGetAttribute"
    bl_label = "Get Instance Attribute"
    nl_category = "Python"
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicPython, 'Parent')
        self.add_input(NodeSocketLogicString, 'Index')
        self.add_output(NodeSocketLogicParameter, 'Child')

    def get_netlogic_class_name(self):
        return "ULGetPyInstanceAttr"

    def get_input_names(self):
        return ['instance', 'attr']

    def get_output_names(self):
        return ['OUT']
