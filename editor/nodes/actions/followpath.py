from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicNavMesh
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicAxis
from ...sockets import NodeSocketLogicAxisSigned


@node_type
class LogicNodeFollowPath(LogicNodeActionType):
    bl_idname = "NLActionFollowPath"
    bl_label = "Follow Path"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULFollowPath"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Moving Object")
        self.add_input(NodeSocketLogicObject, "Rotating Object")
        self.add_input(NodeSocketLogicList, "Path Points")
        self.add_input(NodeSocketLogicBoolean, "Loop")
        self.add_input(NodeSocketLogicBoolean, "Continue")
        self.add_input(NodeSocketLogicNavMesh, "Optional Navmesh")
        self.add_input(NodeSocketLogicBoolean, "Move as Dynamic")
        self.add_input(NodeSocketLogicFloatPositive, "Lin Speed", None, {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloatPositive, "Reach Threshold", None, {'default_value': .2})
        self.add_input(NodeSocketLogicBoolean, "Look At", None, {'default_value': True})
        self.add_input(NodeSocketLogicFloatFactor, "Rot Speed", None, {'default_value': 1.0})
        self.add_input(NodeSocketLogicAxis, "Rot Axis", None, {'default_value': '2'})
        self.add_input(NodeSocketLogicAxisSigned, "Front", None, {'default_value': '1'})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return [
            "condition",
            "moving_object",
            "rotating_object",
            "path_points",
            "loop",
            "path_continue",
            "navmesh_object",
            "move_dynamic",
            "linear_speed",
            "reach_threshold",
            "look_at",
            "rot_speed",
            "rot_axis",
            "front_axis"
        ]
