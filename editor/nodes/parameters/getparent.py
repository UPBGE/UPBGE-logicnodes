from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeGetParent(LogicNodeParameterType):
    bl_idname = "NLParameterGameObjectParent"
    bl_label = "Get Parent"
    bl_description = 'The parent object of an object'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetParent"

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Child Object", 'game_object')
        self.add_output(NodeSocketLogicObject, "Parent Object", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["game_object"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
