from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeGetObject(LogicNodeParameterType):
    bl_idname = "NLActionFindObjectNode"
    bl_label = "Get Object"
    bl_description = 'An object in the scene'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetObject"

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_output(NodeSocketLogicObject, "Object", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["game_object"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
