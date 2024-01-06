from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicXYZ
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeRandomVector(LogicNodeParameterType):
    bl_idname = "NLRandomVect"
    bl_label = "Random Vector"
    nl_module = 'uplogic.nodes.parameters'
    deprecated = True
    deprecation_message = 'Replaced by "Random Value" Node.'

    def init(self, context):
        self.add_input(NodeSocketLogicXYZ, "", None, {'default_value': (True, True, True)})
        self.add_output(NodeSocketLogicVectorXYZ, "Vector")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ['xyz']

    nl_class = "ULRandomVect"

    def get_output_names(self):
        return ["OUT_A"]
