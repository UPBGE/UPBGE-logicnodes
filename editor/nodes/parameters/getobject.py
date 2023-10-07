from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeGetObject(LogicNodeParameterType):
    bl_idname = "NLActionFindObjectNode"
    bl_label = "Get Object"
    bl_icon = 'OBJECT_DATA'
    nl_module = 'parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_output(NodeSocketLogicObject, "Object")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULGetObject"

    def get_input_names(self):
        return ["game_object"]

    def get_output_names(self):
        return ['OUT']
