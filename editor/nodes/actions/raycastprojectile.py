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
    bl_description = 'Perform a raycast that approximates physical behavior'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULProjectileRayCast"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Caster", 'caster', {'use_owner': True})
        self.add_input(NodeSocketLogicVectorXYZ, "Origin", 'origin')
        self.add_input(NodeSocketLogicVectorXYZ, "Aim", 'destination')
        self.add_input(NodeSocketLogicBoolean, 'Local', 'local')
        self.add_input(NodeSocketLogicFloatPositive, "Power", 'power', {'default_value': 10.0})
        self.add_input(NodeSocketLogicFloatPositive, "Distance", 'distance', {'default_value': 20.0})
        self.add_input(NodeSocketLogicFloatFactor, "Resolution", 'resolution', {'default_value': 0.9})
        self.add_input(NodeSocketLogicString, "Property", 'property_name')
        self.add_input(NodeSocketLogicBoolean, 'X-Ray', 'xray')
        self.add_input(NodeSocketLogicBitMask, "Mask", 'mask')
        self.add_input(NodeSocketLogicBoolean, 'Visualize', 'visualize')
        self.add_output(NodeSocketLogicCondition, "Has Result", 'RESULT')
        self.add_output(NodeSocketLogicObject, "Picked Object", 'PICKED_OBJECT')
        self.add_output(NodeSocketLogicVectorXYZ, "Picked Point", 'POINT')
        self.add_output(NodeSocketLogicVectorXYZ, "Picked Normal", 'NORMAL')
        self.add_output(NodeSocketLogicList, "Parabola", 'PARABOLA')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
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

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['RESULT', "PICKED_OBJECT", "POINT", "NORMAL", 'PARABOLA']
