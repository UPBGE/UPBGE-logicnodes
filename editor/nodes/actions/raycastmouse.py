from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicCamera
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVector
from ...sockets import NodeSocketLogicBitMask


@node_type
class LogicNodeRaycastMouse(LogicNodeActionType):
    bl_idname = "NLActionMousePickNode"
    bl_label = "Mouse Ray"
    bl_description = 'Perform a raycast from the camera to where the mouse is pointing'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULMouseRayCast"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicCamera, "Camera", 'camera', {'enabled': False})
        self.add_input(NodeSocketLogicString, "Property", 'property')
        self.add_input(NodeSocketLogicBoolean, 'X-Ray', 'xray')
        self.add_input(NodeSocketLogicFloat, "Distance", 'distance', {'default_value': 100})
        self.add_input(NodeSocketLogicBitMask, "Mask", 'mask')
        self.add_output(NodeSocketLogicCondition, "Has Result", 'RESULT')
        self.add_output(NodeSocketLogicObject, "Picked Object", 'OUTOBJECT')
        self.add_output(NodeSocketLogicVector, "Picked Point", 'OUTPOINT')
        self.add_output(NodeSocketLogicVector, "Picked Normal", 'OUTNORMAL')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "camera", "property", 'xray', "distance", 'mask']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['RESULT', "OUTOBJECT", "OUTPOINT", "OUTNORMAL"]
