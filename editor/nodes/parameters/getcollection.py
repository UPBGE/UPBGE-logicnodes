from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCollection


@node_type
class LogicNodeGetGetCollection(LogicNodeParameterType):
    bl_idname = "NLGetCollectionNode"
    bl_label = "Get Collection"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetCollection"

    def init(self, context):
        self.add_input(NodeSocketLogicCollection, '')
        self.add_output(NodeSocketLogicCollection, "Collection")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ['collection']

    def get_output_names(self):
        return ["OUT"]
