from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCollection


@node_type
class LogicNodeGetGetCollection(LogicNodeParameterType):
    bl_idname = "NLGetCollectionNode"
    bl_label = "Get Collection"
    bl_icon = 'OUTLINER_COLLECTION'
    nl_module = 'parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicCollection, '')
        self.add_output(NodeSocketLogicCollection, "Collection")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ['collection']

    nl_class = "ULGetCollection"

    def get_output_names(self):
        return ["OUT"]
