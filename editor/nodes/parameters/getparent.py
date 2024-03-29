from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeGetParent(LogicNodeParameterType):
    bl_idname = "NLParameterGameObjectParent"
    bl_label = "Get Parent"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetParent"

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Child Object")
        self.add_output(NodeSocketLogicObject, "Parent Object")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["game_object"]

    def get_output_names(self):
        return ["OUT"]
