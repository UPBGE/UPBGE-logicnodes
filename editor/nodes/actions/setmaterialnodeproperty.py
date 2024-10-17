from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicMaterial
from ...sockets import NodeSocketLogicTreeNode
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicValue


@node_type
class LogicNodeSetMaterialNodeProperty(LogicNodeActionType):
    bl_idname = "NLSetMaterialNodeAttribute"
    bl_label = "Set Node Value"
    bl_description = 'Set a value on a material node'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetMatNodeValue"

    search_tags = [
        ['Set Material Node Property', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicMaterial, 'Material', 'mat_name')
        self.add_input(NodeSocketLogicTreeNode, 'Node Name', 'node_name', {'ref_index': 1})
        self.add_input(NodeSocketLogicString, "Internal", 'internal')
        self.add_input(NodeSocketLogicString, "Attribute", 'attribute')
        self.add_input(NodeSocketLogicValue, '', 'value')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        LogicNodeActionType.init(self, context)

    def update_draw(self, context=None):
        if not self.ready:
            return
        mat = self.inputs[1]
        nde = self.inputs[2]
        att = self.inputs[3]
        itl = self.inputs[4]
        val = self.inputs[5]
        if (mat.default_value or mat.is_linked) and (nde.default_value or nde.is_linked):
            att.enabled = val.enabled = itl.enabled = True
        else:
            att.enabled = val.enabled = itl.enabled = False

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "mat_name",
            'node_name',
            'internal',
            "attribute",
            'value'
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
