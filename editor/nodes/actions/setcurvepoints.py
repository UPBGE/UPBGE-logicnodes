from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicCurve


@node_type
class LogicNodeSetCurvePoints(LogicNodeActionType):
    bl_idname = "NLSetCurvePoints"
    bl_label = "Set Curve Points"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetCurvePoints"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicCurve, "Curve")
        self.add_input(NodeSocketLogicList, "Points")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "curve_object", "points"]
