from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicInteger


@node_type
class LogicNodeChildByIndex(LogicNodeParameterType):
    bl_idname = "NLParameterFindChildByIndexNode"
    bl_label = "Get Child By Index"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULChildByIndex"

    def init(self, context):
        self.add_input(NodeSocketLogicObject, 'Parent')
        self.add_input(NodeSocketLogicInteger, 'Index')
        self.add_output(NodeSocketLogicObject, 'Child')
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["from_parent", "index"]

    def get_output_names(self):
        return ['CHILD']
