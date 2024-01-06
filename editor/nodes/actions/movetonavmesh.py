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
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULMoveToWithNavmesh"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Moving Object")
        self.add_input(NodeSocketLogicObject, "Rotating Object")
        self.add_input(NodeSocketLogicNavMesh, "Navmesh Object")
        self.add_input(NodeSocketLogicVectorXYZ, "Destination")
        self.add_input(NodeSocketLogicBoolean, "Move as Dynamic")
        self.add_input(NodeSocketLogicFloatPositive, "Lin Speed", None, {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloatPositive, "Reach Threshold", None, {'default_value': 1.0})
        self.add_input(NodeSocketLogicBoolean, "Look At", None, {'default_value': True})
        self.add_input(NodeSocketLogicAxis, "Rot Axis")
        self.add_input(NodeSocketLogicAxisSigned, "Front")
        self.add_input(NodeSocketLogicFloat, "Rot Speed", None, {'default_value': 1.0})
        self.add_input(NodeSocketLogicBoolean, "Visualize")
        self.add_output(NodeSocketLogicCondition, "Done")
        self.add_output(NodeSocketLogicCondition, "When Reached")
        self.add_output(NodeSocketLogicList, "Next Point")
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT", "FINISHED", "POINT"]

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
