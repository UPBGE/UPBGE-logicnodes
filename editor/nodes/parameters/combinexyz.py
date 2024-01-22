from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeCombineXYZ(LogicNodeParameterType):
    bl_idname = "NLParameterVector3SimpleNode"
    bl_label = "Combine XYZ"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULVectorXYZ"

    search_tags = [
        ['Combine XYZ', {}],
        ['Vector XYZ', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, 'X', 'input_x')
        self.add_input(NodeSocketLogicFloat, 'Y', 'input_y')
        self.add_input(NodeSocketLogicFloat, 'Z', 'input_z')
        self.add_output(NodeSocketLogicVectorXYZ, "Vector", 'OUTV')
        LogicNodeParameterType.init(self, context)

    # def get_output_names(self):
    #     return ["OUTV"]

    # def get_input_names(self):
    #     return ["input_x", "input_y", "input_z"]
