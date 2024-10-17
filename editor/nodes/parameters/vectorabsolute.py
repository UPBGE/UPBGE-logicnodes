from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeVectorAbsolute(LogicNodeParameterType):
    bl_idname = "NLParameterAbsVector3Node"
    bl_label = "Absolute Vector"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULVectorAbsolute"
    deprecated = True
    deprecation_message = 'Included in Vector Math node.'

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, 'Vector', 'input_v')
        self.add_output(NodeSocketLogicVectorXYZ, "Vector", 'OUTV')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUTV"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["input_v"]