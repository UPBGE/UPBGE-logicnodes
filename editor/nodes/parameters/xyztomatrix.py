from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicMatrix


@node_type
class LogicNodeXYZtoMatrix(LogicNodeParameterType):
    bl_idname = "NLParameterEulerToMatrixNode"
    bl_label = "XYZ To Matrix"
    bl_description = 'Construct a Matrix from a 3D vector or Euler'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULEulerToMatrix"

    def init(self, context):
        self.add_input(NodeSocketLogicVectorXYZ, 'XYZ', 'input_e')
        self.add_output(NodeSocketLogicMatrix, "Matrix", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["input_e"]
