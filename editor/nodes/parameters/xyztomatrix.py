from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicMatrix


@node_type
class LogicNodeXYZtoMatrix(LogicNodeParameterType):
    bl_idname = "NLParameterEulerToMatrixNode"
    bl_label = "XYZ To Matrix"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicVectorXYZ, 'XYZ')
        self.add_output(NodeSocketLogicMatrix, "Matrix")

    def get_netlogic_class_name(self):
        return "ULEulerToMatrix"

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["input_e"]
