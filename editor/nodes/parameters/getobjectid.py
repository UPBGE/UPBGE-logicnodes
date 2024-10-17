from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeGetObjectID(LogicNodeParameterType):
    bl_idname = "NLGetObjectDataName"
    bl_label = "Get Object ID"
    bl_description = 'The internal ID name of an object (e.g. "Cube.001")'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULObjectDataName"

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_output(NodeSocketLogicString, "ID", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["game_object"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
