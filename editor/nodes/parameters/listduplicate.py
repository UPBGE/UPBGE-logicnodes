from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeListDuplicate(LogicNodeParameterType):
    bl_idname = "NLDuplicateList"
    bl_label = "Duplicate"
    bl_description = 'Copy a list'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULListDuplicate"

    search_tags = [
        ['Duplicate List', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicList, "List", 'items')
        self.add_output(NodeSocketLogicList, "List", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["items"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
