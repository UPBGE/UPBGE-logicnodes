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


@node_type
class LogicNodeRaycastCamera(LogicNodeActionType):
    bl_idname = "NLActionCameraPickNode"
    bl_label = "Camera Ray"
    bl_description = 'Perform a raycast from the camera into the scene'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULCameraRayCast"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicCamera, "Camera", 'camera', {'use_active': True, 'enabled': False})
        self.add_input(NodeSocketLogicVectorXY, "Aim", 'aim', {'default_value': (.5, .5)})
        self.add_input(NodeSocketLogicString, "Property", 'property_name')
        self.add_input(NodeSocketLogicBoolean, 'X-Ray', 'xray')
        self.add_input(NodeSocketLogicFloat, "Distance", 'distance', {'default_value': 100})
        self.add_input(NodeSocketLogicBitMask, "Mask", 'mask')
        self.add_output(NodeSocketLogicCondition, "Has Result", 'RESULT')
        self.add_output(NodeSocketLogicObject, "Picked Object", 'PICKED_OBJECT')
        self.add_output(NodeSocketLogicVector, "Picked Point", 'PICKED_POINT')
        self.add_output(NodeSocketLogicVector, "Picked Normal", 'PICKED_NORMAL')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
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

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['RESULT', "PICKED_OBJECT", "PICKED_POINT", "PICKED_NORMAL"]
