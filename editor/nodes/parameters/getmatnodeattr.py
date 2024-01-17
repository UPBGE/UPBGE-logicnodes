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
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetMaterialAttribute"

    def init(self, context):
        self.add_input(NodeSocketLogicMaterial, 'Material')
        self.add_input(NodeSocketLogicTreeNode, 'Node Name')
        self.add_input(NodeSocketLogicString, "Internal")
        self.add_input(NodeSocketLogicString, "Attribute")
        self.add_output(NodeSocketLogicParameter, "Value")
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

    def get_input_names(self):
        return ["mat_name", 'node_name', "internal", 'attribute']

    def get_output_names(self):
        return ['OUT']
