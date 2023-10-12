from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeGetObjectID(LogicNodeParameterType):
    bl_idname = "NLGetObjectDataName"
    bl_label = "Get Object ID"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_output(NodeSocketLogicString, "ID")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULObjectDataName"

    def get_input_names(self):
        return ["game_object"]

    def get_output_names(self):
        return ["OUT"]
