from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeListDuplicate(LogicNodeParameterType):
    bl_idname = "NLDuplicateList"
    bl_label = "Duplicate"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULListDuplicate"

    search_tags = [
        ['Duplicate List', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicList, "List")
        self.add_output(NodeSocketLogicList, "List")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["items"]

    def get_output_names(self):
        return ['OUT']
