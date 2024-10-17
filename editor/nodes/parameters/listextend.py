from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeListExtend(LogicNodeParameterType):
    bl_idname = "NLExtendList"
    bl_label = "Extend"
    bl_description = 'Extend a list by another'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULListExtend"

    search_tags = [
        ['List Extend', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicList, 'List 1', 'list_1')
        self.add_input(NodeSocketLogicList, 'List 2', 'list_2')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT', {'enabled': False})
        self.add_output(NodeSocketLogicList, 'List', 'LIST')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", "LIST"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['list_1', 'list_2']

