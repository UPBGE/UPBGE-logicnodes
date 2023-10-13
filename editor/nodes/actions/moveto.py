from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeMoveTo(LogicNodeActionType):
    bl_idname = "NLActionMoveTo"
    bl_label = "Move To"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULMoveTo"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicVectorXYZ, "Target Location")
        self.add_input(NodeSocketLogicBoolean, "Move as Dynamic")
        self.add_input(NodeSocketLogicFloatPositive, "Speed", {'value': 1.0})
        self.add_input(NodeSocketLogicFloat, "Stop At Distance", {'value': 0.5})
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return [
            "condition",
            "moving_object",
            "destination_point",
            'dynamic',
            "speed",
            "distance"
        ]
