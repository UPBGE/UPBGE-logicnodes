from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicImage
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicUI


@node_type
class LogicNodeSetCustomCursor(LogicNodeActionType):
    bl_idname = "LogicNodeSetCustomCursor"
    bl_label = "Set Custom Cursor"
    bl_description = 'Bind an image to the mouse cursor'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetCustomCursor"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicImage, "Texture", 'texture')
        self.add_input(NodeSocketLogicVectorXY, "Size", 'size', {'default_value': (30., 30.)})
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        self.add_output(NodeSocketLogicUI, "Cursor", 'CURSOR')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", 'CURSOR']

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "texture", "size"]
