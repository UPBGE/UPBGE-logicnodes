from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicCurve
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicNavMesh
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicAxis
from ...sockets import NodeSocketLogicAxisSigned
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeFollowCurve(LogicNodeActionType):
    bl_idname = "LogicNodeFollowPath"
    bl_label = "Follow Path"
    bl_description = 'Move an object along a curve'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "FollowCurveNode"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicCurve, "Curve", 'curve')
        self.add_input(NodeSocketLogicBoolean, "Loop", 'loop')
        self.add_input(NodeSocketLogicBoolean, "Continue", 'path_continue')
        self.add_input(NodeSocketLogicFloatPositive, "Speed", 'speed', {'default_value': 1.0})
        self.add_input(NodeSocketLogicBoolean, "Look At", 'look_at', {'default_value': True})
        self.add_input(NodeSocketLogicAxis, "Rotation Axis", 'rot_axis', {'default_value': '2'})
        self.add_input(NodeSocketLogicAxisSigned, "Front", 'front_axis', {'default_value': '1'})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)
