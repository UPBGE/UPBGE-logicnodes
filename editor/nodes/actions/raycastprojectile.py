from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicBitMask


@node_type
class LogicNodeRaycastProjectile(LogicNodeActionType):
    bl_idname = "NLProjectileRayCast"
    bl_label = "Projectile Ray"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULProjectileRayCast"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicVectorXYZ, "Origin")
        self.add_input(NodeSocketLogicVectorXYZ, "Aim")
        self.add_input(NodeSocketLogicBoolean, 'Local')
        self.add_input(NodeSocketLogicFloatPositive, "Power", None, {'default_value': 10.0})
        self.add_input(NodeSocketLogicFloatPositive, "Distance", None, {'default_value': 20.0})
        self.add_input(NodeSocketLogicFloatFactor, "Resolution", None, {'default_value': 0.9})
        self.add_input(NodeSocketLogicString, "Property")
        self.add_input(NodeSocketLogicBoolean, 'X-Ray')
        self.add_input(NodeSocketLogicBitMask, "Mask")
        self.add_input(NodeSocketLogicBoolean, 'Visualize')
        self.add_output(NodeSocketLogicCondition, "Has Result")
        self.add_output(NodeSocketLogicObject, "Picked Object")
        self.add_output(NodeSocketLogicVectorXYZ, "Picked Point")
        self.add_output(NodeSocketLogicVectorXYZ, "Picked Normal")
        self.add_output(NodeSocketLogicList, "Parabola")
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return [
            "condition",
            "origin",
            "destination",
            'local',
            'power',
            'distance',
            "resolution",
            "property_name",
            'xray',
            'mask',
            "visualize"
        ]

    def get_output_names(self):
        return ['RESULT', "PICKED_OBJECT", "POINT", "NORMAL", 'PARABOLA']
