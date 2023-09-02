from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCollection
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeGetCollectionObjects(LogicNodeParameterType):
    bl_idname = "NLGetCollectionObjectsNode"
    bl_label = "Get Objects"
    nl_category = "Scene"
    nl_subcat = 'Collections'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicCollection, 'Collection')
        self.add_output(NodeSocketLogicList, "Objects")

    def get_input_names(self):
        return ['collection']

    def get_netlogic_class_name(self):
        return "ULGetCollectionObjects"

    def get_output_names(self):
        return ["OUT"]
