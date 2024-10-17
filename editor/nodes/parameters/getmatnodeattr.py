from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicTreeNode
from ...sockets import NodeSocketLogicMaterial
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeGetMaterialNodeAttr(LogicNodeParameterType):
    bl_idname = "NLGetMaterialNodeAttribute"
    bl_label = "Get Node Value"
    bl_description = 'An attribute of a shader node'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetMaterialAttribute"

    def init(self, context):
        self.add_input(NodeSocketLogicMaterial, 'Material', 'mat_name')
        self.add_input(NodeSocketLogicTreeNode, 'Node Name', 'node_name')
        self.add_input(NodeSocketLogicString, "Internal", 'internal')
        self.add_input(NodeSocketLogicString, "Attribute", 'attribute')
        self.add_output(NodeSocketLogicParameter, "Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    def update_draw(self, context=None):
        if not self.ready:
            return
        mat = self.inputs[0]
        nde = self.inputs[1]
        itl = self.inputs[2]
        att = self.inputs[3]
        if (mat.default_value or mat.is_linked) and (nde.default_value or nde.is_linked):
            itl.enabled = att.enabled = True
        else:
            itl.enabled = att.enabled = False

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["mat_name", 'node_name', "internal", 'attribute']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
