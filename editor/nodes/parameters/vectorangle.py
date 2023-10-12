from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeVectorAngle(LogicNodeParameterType):
    bl_idname = "NLVectorAngle"
    bl_label = "Angle"
    nl_module = 'uplogic.nodes.parameters'
    deprecated = True
    deprecation_message = 'Replaced by "Vector Math" Node.'

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 1")
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 2")
        self.add_output(NodeSocketLogicFloat, 'Angle')
        LogicNodeParameterType.init(self, context)

    nl_class = "ULVectorAngle"

    def get_input_names(self):
        return ["vector", 'vector_2']

    def get_output_names(self):
        return ['OUT']
