from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloat
from ....utilities import deprecate


@node_type
class LogicNodeVectorAngle(LogicNodeParameterType):
    bl_idname = "NLVectorAngle"
    bl_label = "Angle"
    nl_category = "Math"
    nl_subcat = 'Vector Math'
    nl_module = 'parameters'
    deprecated = True

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        # deprecate(self)
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 1")
        self.add_input(NodeSocketLogicVectorXYZ, "Vector 2")
        self.add_output(NodeSocketLogicFloat, 'Angle')

    def get_netlogic_class_name(self):
        return "ULVectorAngle"

    def get_input_names(self):
        # deprecate(self)
        return ["vector", 'vector_2']

    def get_output_names(self):
        return ['OUT']
