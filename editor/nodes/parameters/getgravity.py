from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeGetGravity(LogicNodeParameterType):
    bl_idname = "NLGetGravityNode"
    bl_label = "Get Gravity"
    bl_description = 'Scene gravity vector'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetGravity"

    def init(self, context):
        self.add_output(NodeSocketLogicVectorXYZ, "Gravity", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
