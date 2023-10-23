from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeListExtend(LogicNodeParameterType):
    bl_idname = "NLExtendList"
    bl_label = "Extend"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULListExtend"

    search_tags = [
        ['List Extend', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicList, 'List 1')
        self.add_input(NodeSocketLogicList, 'List 2')
        self.add_output(NodeSocketLogicCondition, 'Done', {'enabled': False})
        self.add_output(NodeSocketLogicList, 'List')
        LogicNodeParameterType.init(self, context)

    def get_output_names(self):
        return ["OUT", "LIST"]

    def get_input_names(self):
        return ['list_1', 'list_2']

