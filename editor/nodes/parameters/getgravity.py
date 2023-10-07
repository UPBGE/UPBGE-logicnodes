from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeGetGravity(LogicNodeParameterType):
    bl_idname = "NLGetGravityNode"
    bl_label = "Get Gravity"
    nl_module = 'parameters'

    def init(self, context):
        self.add_output(NodeSocketLogicVectorXYZ, "Gravity")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULGetGravity"

    def get_output_names(self):
        return ["OUT"]
