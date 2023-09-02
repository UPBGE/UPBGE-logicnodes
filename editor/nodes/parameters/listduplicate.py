from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeListDuplicate(LogicNodeParameterType):
    bl_idname = "NLDuplicateList"
    bl_label = "Duplicate"
    bl_icon = 'CON_TRANSLIKE'
    nl_category = "Data"
    nl_subcat = 'List'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicList, "List")
        self.add_output(NodeSocketLogicList, "List")

    def get_netlogic_class_name(self):
        return "ULListDuplicate"

    def get_input_names(self):
        return ["items"]

    def get_output_names(self):
        return ['OUT']
