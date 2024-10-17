from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCollection


@node_type
class LogicNodeGetGetCollection(LogicNodeParameterType):
    bl_idname = "NLGetCollectionNode"
    bl_label = "Get Collection"
    bl_description = 'Collection (ID)'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetCollection"

    def init(self, context):
        self.add_input(NodeSocketLogicCollection, '', 'collection')
        self.add_output(NodeSocketLogicCollection, "Collection", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['collection']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
