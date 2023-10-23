from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCollection
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeGetCollectionObjectNames(LogicNodeParameterType):
    bl_idname = "NLGetCollectionObjectNamesNode"
    bl_label = "Get Object Names"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicCollection, 'Collection')
        self.add_output(NodeSocketLogicList, "Object Names")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ['collection']

    nl_class = "ULGetCollectionObjectNames"

    def get_output_names(self):
        return ["OUT"]
