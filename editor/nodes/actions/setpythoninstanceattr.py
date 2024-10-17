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
    bl_description = 'Set an attribute of a python object instance'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetPyInstanceAttr"

    search_tags = [
        ['Set Python Instance Attribute', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicPython, "Object Instance", 'instance')
        self.add_input(NodeSocketLogicString, "Attribute", 'attr')
        self.add_input(NodeSocketLogicValue, "", 'value')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['condition', 'instance', 'attr', 'value']
