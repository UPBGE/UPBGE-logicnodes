from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicMatrix


@node_type
class LogicNodeXYZtoMatrix(LogicNodeParameterType):
    bl_idname = "NLParameterEulerToMatrixNode"
    bl_label = "XYZ To Matrix"
    nl_module = 'parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, 'XYZ')
        self.add_output(NodeSocketLogicMatrix, "Matrix")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULEulerToMatrix"

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["input_e"]
