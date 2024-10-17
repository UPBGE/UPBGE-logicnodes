from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCollection
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeGetCollectionObjects(LogicNodeParameterType):
    bl_idname = "NLGetCollectionObjectsNode"
    bl_label = "Get Objects"
    bl_description = 'List of objects in a collection'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetCollectionObjects"

    def init(self, context):
        self.add_input(NodeSocketLogicCollection, 'Collection', 'collection')
        self.add_output(NodeSocketLogicList, "Objects", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['collection']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
