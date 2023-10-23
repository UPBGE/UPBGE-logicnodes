from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeGetObject(LogicNodeParameterType):
    bl_idname = "NLActionFindObjectNode"
    bl_label = "Get Object"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetObject"

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_output(NodeSocketLogicObject, "Object")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["game_object"]

    def get_output_names(self):
        return ['OUT']
