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
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULMouseRayCast"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicCamera, "Camera", {'enabled': False})
        self.add_input(NodeSocketLogicString, "Property")
        self.add_input(NodeSocketLogicBoolean, 'X-Ray')
        self.add_input(NodeSocketLogicFloat, "Distance", {'default_value': 100})
        self.add_input(NodeSocketLogicBitMask, "Mask", {'value': 100})
        self.add_output(NodeSocketLogicCondition, "Has Result")
        self.add_output(NodeSocketLogicObject, "Picked Object")
        self.add_output(NodeSocketLogicVector, "Picked Point")
        self.add_output(NodeSocketLogicVector, "Picked Normal")
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ["condition", "camera", "property", 'xray', "distance", 'mask']

    def get_output_names(self):
        return ['RESULT', "OUTOBJECT", "OUTPOINT", "OUTNORMAL"]
