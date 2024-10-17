from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicCollection
from ...sockets import NodeSocketLogicBoolean


@node_type
class LogicNodeSetCollectionVisibility(LogicNodeActionType):
    bl_idname = "NLActionSetCollectionVisibility"
    bl_label = "Set Collection Visibility"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetCollectionVisibility"
    bl_description = 'Set the visibility of all objects in a collection'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicCollection, "Collection", 'collection')
        self.add_input(NodeSocketLogicBoolean, "Visible", 'visible')
        self.add_input(NodeSocketLogicBoolean, "Include Children", 'recursive')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "collection", "visible", "recursive"]
