from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicCollection


@node_type
class LogicNodeRemoveOverlayCollection(LogicNodeActionType):
    bl_idname = "NLRemoveOverlayCollection"
    bl_label = "Remove Overlay Collection"
    nl_module = 'uplogic.nodes.actions'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicCollection, 'Collection')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_input_names(self):
        return ['condition', 'collection']

    nl_class = "ULRemoveOverlayCollection"
