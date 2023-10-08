from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicPython


@node_type
class LogicNodeSetPythonInstanceAttr(LogicNodeActionType):
    bl_idname = "NLParameterSetAttribute"
    bl_label = "Set Object Attribute"
    nl_category = "Python"
    nl_module = 'actions'
    nl_class = "ULSetPyInstanceAttr"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicPython, "Object Instance")
        self.add_input(NodeSocketLogicString, "Attribute")
        self.add_input(NodeSocketLogicValue, "")
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ['condition', 'instance', 'attr', 'value']
