from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCollection


@node_type
class LogicNodeGetGetCollection(LogicNodeParameterType):
    bl_idname = "NLGetCollectionNode"
    bl_label = "Get Collection"
    bl_icon = 'OUTLINER_COLLECTION'
    nl_category = "Scene"
    nl_subcat = 'Collections'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicCollection, '')
        self.add_output(NodeSocketLogicCollection, "Collection")

    def get_input_names(self):
        return ['collection']

    def get_netlogic_class_name(self):
        return "ULGetCollection"

    def get_output_names(self):
        return ["OUT"]
