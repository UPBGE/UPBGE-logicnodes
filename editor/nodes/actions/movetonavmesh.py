from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicNavMesh
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicAxis
from ...sockets import NodeSocketLogicAxisSigned
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeMoveToNavmesh(LogicNodeActionType):
    bl_idname = "NLActionNavigate"
    bl_label = "Move To with Navmesh"
    bl_description = 'Move an object to a point at constant speed using a navmesh'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULMoveToWithNavmesh"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Moving Object", 'moving_object')
        self.add_input(NodeSocketLogicObject, "Rotating Object", 'rotating_object')
        self.add_input(NodeSocketLogicNavMesh, "Navmesh Object", 'navmesh_object')
        self.add_input(NodeSocketLogicVectorXYZ, "Destination", 'destination_point')
        self.add_input(NodeSocketLogicBoolean, "Move as Dynamic", 'move_dynamic')
        self.add_input(NodeSocketLogicFloatPositive, "Lin Speed", 'linear_speed', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloatPositive, "Reach Threshold", 'reach_threshold', {'default_value': 1.0})
        self.add_input(NodeSocketLogicBoolean, "Look At", 'look_at', {'default_value': True})
        self.add_input(NodeSocketLogicAxis, "Rot Axis", 'rot_axis')
        self.add_input(NodeSocketLogicAxisSigned, "Front", 'front_axis')
        self.add_input(NodeSocketLogicFloat, "Rot Speed", 'rot_speed', {'default_value': 1.0})
        self.add_input(NodeSocketLogicBoolean, "Visualize", 'visualize')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        self.add_output(NodeSocketLogicCondition, "When Reached", 'FINISHED')
        self.add_output(NodeSocketLogicList, "Next Point", 'POINT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", "FINISHED", "POINT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "moving_object",
            "rotating_object",
            "navmesh_object",
            "destination_point",
            "move_dynamic",
            "linear_speed",
            "reach_threshold",
            "look_at",
            "rot_axis",
            "front_axis",
            "rot_speed",
            'visualize'
        ]
