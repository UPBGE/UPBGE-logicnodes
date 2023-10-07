from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicNodeGroupNode
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicNodeGroup
from ...sockets import NodeSocketLogicValue


@node_type
class LogicNodeSetNodeGroupNodeProperty(LogicNodeActionType):
    bl_idname = "NLSetNodeTreeNodeAttribute"
    bl_label = "Set Node Value"
    bl_icon = 'DRIVER_TRANSFORM'
    nl_category = 'Nodes'
    nl_subcat = 'Groups'
    nl_module = 'actions'
    deprecated = True

    search_tags = [
        ['Set Node Group Node Property', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicNodeGroup, 'Tree')
        self.add_input(NodeSocketLogicNodeGroupNode, 'Node Name', {'ref_index': 1})
        self.add_input(NodeSocketLogicString, "Internal")
        self.add_input(NodeSocketLogicString, "Attribute")
        self.add_input(NodeSocketLogicValue, '')
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def update_draw(self, context=None):
        if not self.ready:
            return
        tree = self.inputs[1]
        nde = self.inputs[2]
        att = self.inputs[3]
        itl = self.inputs[4]
        val = self.inputs[5]
        if (tree.value or tree.is_linked) and (nde.value or nde.is_linked):
            att.enabled = val.enabled = itl.enabled = True
        else:
            att.enabled = val.enabled = itl.enabled = False

    nl_class = "ULSetNodeValue"

    def get_input_names(self):
        return [
            "condition",
            "tree_name",
            'node_name',
            'internal',
            "attribute",
            'value'
        ]

    def get_output_names(self):
        return ['OUT']
