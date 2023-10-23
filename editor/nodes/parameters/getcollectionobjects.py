from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCollection
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeGetCollectionObjects(LogicNodeParameterType):
    bl_idname = "NLGetCollectionObjectsNode"
    bl_label = "Get Objects"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicCollection, 'Collection')
        self.add_output(NodeSocketLogicList, "Objects")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ['collection']

    nl_class = "ULGetCollectionObjects"

    def get_output_names(self):
        return ["OUT"]
