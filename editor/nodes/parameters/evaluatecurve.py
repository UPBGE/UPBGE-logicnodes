from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicCurve
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeEvaluateCurve(LogicNodeParameterType):
    bl_idname = "LogicNodeEvaluateCurve"
    bl_label = "Evaluate Curve"
    bl_description = 'Get the point on a curve at a given factor'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "EvaluateCurveNode"

    def init(self, context):
        self.add_input(NodeSocketLogicCurve, 'Curve', 'curve')
        self.add_input(NodeSocketLogicFloat, 'Factor', 'factor')
        self.add_output(NodeSocketLogicVectorXYZ, "Vector", 'VEC')
        LogicNodeParameterType.init(self, context)
