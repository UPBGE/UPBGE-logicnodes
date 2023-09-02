from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeGetGravity(LogicNodeParameterType):
    bl_idname = "NLGetGravityNode"
    bl_label = "Get Gravity"
    nl_category = "Scene"
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_output(NodeSocketLogicVectorXYZ, "Gravity")

    def get_netlogic_class_name(self):
        return "ULGetGravity"

    def get_output_names(self):
        return ["OUT"]
