from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicCamera
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeSetCameraOrthoScale(LogicNodeActionType):
    bl_idname = "NLActionSetCameraOrthoScale"
    bl_label = "Set Orthographic Scale"
    bl_description = 'Set the scale on an orthographic camera'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetCameraOrthoScale"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicCamera, 'Camera', 'camera')
        self.add_input(NodeSocketLogicFloat, 'Scale', 'scale', {'default_value': 1.0})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "camera", 'scale']
