from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeGetObjectVertices(LogicNodeParameterType):
    bl_idname = "NLGetObjectVertices"
    bl_label = "Get Object Vertices"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_output(NodeSocketLogicList, "Vertices")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULObjectDataVertices"

    def get_input_names(self):
        return ["game_object"]

    def get_output_names(self):
        return ["OUT"]
