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

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Collider")
        self.add_input(NodeSocketLogicFloat, "Suspension", {'value': .06})
        self.add_input(NodeSocketLogicFloat, "Stiffness", {'value': 50})
        self.add_input(NodeSocketLogicFloat, "Damping", {'value': 5})
        self.add_input(NodeSocketLogicFloat, "Friction", {'value': 2})
        self.add_input(NodeSocketLogicFloatPositive, "Wheel Modifier", {'value': 1})
        self.add_output(NodeSocketLogicCondition, 'Done')
        self.add_output(NodeSocketLogicPython, 'Vehicle Constraint')
        self.add_output(NodeSocketLogicList, 'Wheels')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT", 'VEHICLE', 'WHEELS']


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
