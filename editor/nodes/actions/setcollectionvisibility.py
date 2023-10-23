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

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicCollection, "Collection")
        self.add_input(NodeSocketLogicBoolean, "Visible")
        self.add_input(NodeSocketLogicBoolean, "Include Children")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "collection", "visible", "recursive"]
