from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCurve
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeGetCurvePoints(LogicNodeParameterType):
    bl_idname = "NLGetCurvePoints"
    bl_label = "Get Curve Points"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetCurvePoints"

    def init(self, context):
        self.add_input(NodeSocketLogicCurve, "Curve")
        self.add_output(NodeSocketLogicList, "Points")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["curve"]

    def get_output_names(self):
        return ["OUT"]
