from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCurve
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeGetCurvePoints(LogicNodeParameterType):
    bl_idname = "NLGetCurvePoints"
    bl_label = "Get Curve Points"
    bl_description = 'List of curve points in world space'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetCurvePoints"

    def init(self, context):
        self.add_input(NodeSocketLogicCurve, "Curve", 'curve')
        self.add_output(NodeSocketLogicVectorXYZ, "Points", 'OUT', shape='SQUARE')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["curve"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]
