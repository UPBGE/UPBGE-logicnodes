from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicCamera
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVector
from ...sockets import NodeSocketLogicBitMask
from ....utilities import OUTCELL


@node_type
class LogicNodeRaycastCamera(LogicNodeActionType):
    bl_idname = "NLActionCameraPickNode"
    bl_label = "Camera Ray"
    nl_module = 'uplogic.nodes.actions'
    changed = True

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicCamera, "Camera", {'use_active': True, 'enabled': False})
        self.add_input(NodeSocketLogicVectorXY, "Aim", {'value_x': .5, 'value_y': .5})
        self.add_input(NodeSocketLogicString, "Property")
        self.add_input(NodeSocketLogicBoolean, 'X-Ray')
        self.add_input(NodeSocketLogicFloat, "Distance", {'value': 100})
        self.add_input(NodeSocketLogicBitMask, "Mask")
        self.add_output(NodeSocketLogicCondition, "Has Result")
        self.add_output(NodeSocketLogicObject, "Picked Object")
        self.add_output(NodeSocketLogicVector, "Picked Point")
        self.add_output(NodeSocketLogicVector, "Picked Normal")
        LogicNodeActionType.init(self, context)

    nl_class = "ULCameraRayCast"

    def get_input_names(self):
        return [
            "condition",
            "camera",
            "aim",
            "property_name",
            "xray",
            "distance",
            'mask'
        ]

    def get_output_names(self):
        return ['RESULT', "PICKED_OBJECT", "PICKED_POINT", "PICKED_NORMAL"]
