from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicList


@node_type
class LogicNodeVehicleCreate(LogicNodeActionType):
    bl_idname = "NLCreateVehicleFromParent"
    bl_label = "Create New Vehicle"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULCreateVehicle"
    bl_description = (
        'Create a new vehicle from an object. The wheels need to be parented to the'
        'physical body and have either "FWheel" (Front) or "RWheel" (Rear) in their name'
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Collider", 'game_object')
        self.add_input(NodeSocketLogicFloat, "Suspension", 'suspension', {'default_value': .06})
        self.add_input(NodeSocketLogicFloat, "Stiffness", 'stiffness', {'default_value': 50})
        self.add_input(NodeSocketLogicFloat, "Damping", 'damping', {'default_value': 5})
        self.add_input(NodeSocketLogicFloat, "Friction", 'friction', {'default_value': 2})
        self.add_input(NodeSocketLogicFloatPositive, "Wheel Modifier", 'wheel_size', {'default_value': 1})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        self.add_output(NodeSocketLogicPython, 'Vehicle Constraint', 'VEHICLE')
        self.add_output(NodeSocketLogicList, 'Wheels', 'WHEELS')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", 'VEHICLE', 'WHEELS']

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "game_object",
            'suspension',
            'stiffness',
            'damping',
            'friction',
            'wheel_size'
        ]
