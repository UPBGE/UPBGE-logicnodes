from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicNavMesh
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicAxis
from ...sockets import NodeSocketLogicAxisSigned
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeFollowPath(LogicNodeActionType):
    bl_idname = "NLActionFollowPath"
    bl_label = "Follow Path"
    bl_description = 'Move an object along a sequence of points'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULFollowPath"
    # deprecated = True
    # deprecation_message = 'Replaced by newer version.'

    def update_draw(self, context=None):
        look_at = self.inputs[10].default_value
        self.inputs[11].enabled = look_at
        self.inputs[12].enabled = look_at
        self.inputs[13].enabled = look_at

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Moving Object", 'moving_object')
        self.add_input(NodeSocketLogicObject, "Rotating Object", 'rotating_object')
        self.add_input(NodeSocketLogicVectorXYZ, "Path Points", 'path_points', shape='SQUARE', settings={'list_mode': True})
        self.add_input(NodeSocketLogicBoolean, "Loop", 'loop')
        self.add_input(NodeSocketLogicBoolean, "Continue", 'path_continue')
        self.add_input(NodeSocketLogicNavMesh, "Optional Navmesh", 'navmesh_object')
        self.add_input(NodeSocketLogicBoolean, "Move as Dynamic", 'move_dynamic')
        self.add_input(NodeSocketLogicFloatPositive, "Lin Speed", 'linear_speed', {'default_value': 1.0})
        self.add_input(NodeSocketLogicFloatPositive, "Reach Threshold", 'reach_threshold', {'default_value': .2})
        self.add_input(NodeSocketLogicBoolean, "Look At", 'look_at', {'default_value': True})
        self.add_input(NodeSocketLogicFloatFactor, "Rot Speed", 'rot_speed', {'default_value': 1.0})
        self.add_input(NodeSocketLogicAxis, "Rot Axis", 'rot_axis', {'default_value': '2'})
        self.add_input(NodeSocketLogicAxisSigned, "Front", 'front_axis', {'default_value': '1'})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
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


# @node_type
# class LogicNodeFollowPath(LogicNodeActionType):
#     bl_idname = "LogicNodeFollowPath"
#     bl_label = "Follow Path"
#     bl_description = 'Move an object along a curve orsequence of points'
#     nl_module = 'uplogic.nodes.actions'
#     nl_class = "FollowPathNode"

#     def update_draw(self, context=None):
#         look_at = self.inputs[10].default_value
#         self.inputs[11].enabled = look_at
#         self.inputs[12].enabled = look_at
#         self.inputs[13].enabled = look_at

#     def init(self, context):
#         self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
#         self.add_input(NodeSocketLogicObject, "Moving Object", 'moving_object')
#         self.add_input(NodeSocketLogicObject, "Rotating Object", 'rotating_object')
#         self.add_input(NodeSocketLogicVectorXYZ, "Path Points", 'path_points', shape='SQUARE', settings={'list_mode': True})
#         self.add_input(NodeSocketLogicBoolean, "Loop", 'loop')
#         self.add_input(NodeSocketLogicBoolean, "Continue", 'path_continue')
#         self.add_input(NodeSocketLogicNavMesh, "Optional Navmesh", 'navmesh_object')
#         self.add_input(NodeSocketLogicBoolean, "Move as Dynamic", 'move_dynamic')
#         self.add_input(NodeSocketLogicFloatPositive, "Speed", 'linear_speed', {'default_value': 1.0})
#         self.add_input(NodeSocketLogicFloatPositive, "Threshold", 'reach_threshold', {'default_value': .2})
#         self.add_input(NodeSocketLogicBoolean, "Look At", 'look_at', {'default_value': True})
#         self.add_input(NodeSocketLogicFloatFactor, "Rot Speed", 'rot_speed', {'default_value': 1.0})
#         self.add_input(NodeSocketLogicAxis, "Rot Axis", 'rot_axis', {'default_value': '2'})
#         self.add_input(NodeSocketLogicAxisSigned, "Front", 'front_axis', {'default_value': '1'})
#         self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
#         LogicNodeActionType.init(self, context)

#     # XXX: Remove for 5.0
#     def get_output_names(self):
#         return ["OUT"]

#     # XXX: Remove for 5.0
#     def get_input_names(self):
#         return [
#             "condition",
#             "moving_object",
#             "rotating_object",
#             "path_points",
#             "loop",
#             "path_continue",
#             "navmesh_object",
#             "move_dynamic",
#             "linear_speed",
#             "reach_threshold",
#             "look_at",
#             "rot_speed",
#             "rot_axis",
#             "front_axis"
#         ]
