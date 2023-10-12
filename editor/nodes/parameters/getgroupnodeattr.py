from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicNodeGroupNode
from ...sockets import NodeSocketLogicNodeGroup
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeGroupNodeAttr(LogicNodeParameterType):
    bl_idname = "NLGetNodeTreeNodeAttribute"
    bl_label = "Get Node Value"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetNodeAttribute"

    def init(self, context):
        self.add_input(NodeSocketLogicNodeGroup, 'Tree')
        self.add_input(NodeSocketLogicNodeGroupNode, 'Node Name')
        self.add_input(NodeSocketLogicString, "Internal")
        self.add_input(NodeSocketLogicString, "Attribute")
        self.add_output(NodeSocketLogicParameter, "Value")
        LogicNodeParameterType.init(self, context)

    def update_draw(self, context=None):
        tree = self.inputs[0]
        nde = self.inputs[1]
        itl = self.inputs[2]
        att = self.inputs[3]
        if (tree.value or tree.is_linked) and (nde.value or nde.is_linked):
            itl.enabled = att.enabled = True
        else:
            itl.enabled = att.enabled = False

    def get_input_names(self):
        return ["tree_name", 'node_name', "internal", 'attribute']

    def get_output_names(self):
        return ['OUT']
