from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicNodeGroupNode
from ...sockets import NodeSocketLogicGeometryNodeTree
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeGetGeoNodeAttr(LogicNodeParameterType):
    bl_idname = "NLGetGeometryNodeAttribute"
    bl_label = "Get Node Value"
    bl_description = 'Get an attribute from a geometry node'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetNodeAttribute"

    def init(self, context):
        self.add_input(NodeSocketLogicGeometryNodeTree, 'Tree', 'tree_name')
        self.add_input(NodeSocketLogicNodeGroupNode, 'Node Name', 'node_name')
        self.add_input(NodeSocketLogicString, "Internal", 'internal')
        self.add_input(NodeSocketLogicString, "Attribute", 'attribute')
        self.add_output(NodeSocketLogicParameter, "Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    def update_draw(self, context=None):
        if len(self.inputs) < 4:
            return
        tree = self.inputs[0]
        nde = self.inputs[1]
        itl = self.inputs[2]
        att = self.inputs[3]
        if (tree.default_value or tree.is_linked) and (nde.default_value or nde.is_linked):
            itl.enabled = att.enabled = True
        else:
            itl.enabled = att.enabled = False

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["tree_name", 'node_name', "internal", 'attribute']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
