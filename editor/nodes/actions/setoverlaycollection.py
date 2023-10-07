from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicCamera
from ...sockets import NodeSocketLogicCollection


@node_type
class LogicNodeSetOverlayCollection(LogicNodeActionType):
    bl_idname = "NLSetOverlayCollection"
    bl_label = "Set Overlay Collection"
    nl_module = 'actions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicCamera, 'Camera')
        self.add_input(NodeSocketLogicCollection, 'Collection')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ['condition', 'camera', 'collection']

    nl_class = "ULSetOverlayCollection"
