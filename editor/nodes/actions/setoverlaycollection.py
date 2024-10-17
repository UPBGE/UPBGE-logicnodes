from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicCamera
from ...sockets import NodeSocketLogicCollection


@node_type
class LogicNodeSetOverlayCollection(LogicNodeActionType):
    bl_idname = "NLSetOverlayCollection"
    bl_label = "Set Overlay Collection"
    bl_description = 'Add a new overlay collection'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetOverlayCollection"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_input(NodeSocketLogicCamera, 'Camera', 'camera')
        self.add_input(NodeSocketLogicCollection, 'Collection', 'collection')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['condition', 'camera', 'collection']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
