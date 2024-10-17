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
    bl_description = 'Move an object to a point at a constant speed'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULMoveTo"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'moving_object')
        self.add_input(NodeSocketLogicVectorXYZ, "Target Location", 'destination_point')
        self.add_input(NodeSocketLogicBoolean, "Move as Dynamic", 'dynamic')
        self.add_input(NodeSocketLogicFloatPositive, "Speed", 'speed', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloat, "Stop At Distance", 'distance', {'default_value': 0.5})
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        self.add_output(NodeSocketLogicCondition, "Reached", 'REACHED')
        LogicNodeActionType.init(self, context)

    # XXX Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "moving_object",
            "destination_point",
            'dynamic',
            "speed",
            "distance"
        ]
