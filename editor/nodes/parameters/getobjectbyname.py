from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeObjectByName(LogicNodeParameterType):
    bl_idname = "LogicNodeObjectByName"
    bl_label = "Get Object By Name"
    bl_description = 'An object in the scene'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "GetObjectByNameNode"

    def init(self, context):
        self.add_input(NodeSocketLogicString, 'Name', 'object_name')
        self.add_output(NodeSocketLogicObject, 'Object', 'GAME_OBJECT')
        LogicNodeParameterType.init(self, context)
