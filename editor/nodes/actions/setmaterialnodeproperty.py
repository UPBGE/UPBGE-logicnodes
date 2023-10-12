from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicMaterial
from ...sockets import NodeSocketLogicMaterialNode
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicValue


@node_type
class LogicNodeSetMaterialNodeProperty(LogicNodeActionType):
    bl_idname = "NLSetMaterialNodeAttribute"
    bl_label = "Set Node Value"
    nl_module = 'uplogic.nodes.actions'
    # deprecated = True

    search_tags = [
        ['Set Material Node Property', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicMaterial, 'Material')
        self.add_input(NodeSocketLogicMaterialNode, 'Node Name', {'ref_index': 1})
        self.add_input(NodeSocketLogicString, "Internal")
        self.add_input(NodeSocketLogicString, "Attribute")
        self.add_input(NodeSocketLogicValue, '')
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def update_draw(self, context=None):
        if not self.ready:
            return
        mat = self.inputs[1]
        nde = self.inputs[2]
        att = self.inputs[3]
        itl = self.inputs[4]
        val = self.inputs[5]
        if (mat.value or mat.is_linked) and (nde.value or nde.is_linked):
            att.enabled = val.enabled = itl.enabled = True
        else:
            att.enabled = val.enabled = itl.enabled = False

    nl_class = "ULSetMatNodeValue"

    def get_input_names(self):
        return [
            "condition",
            "mat_name",
            'node_name',
            'internal',
            "attribute",
            'value'
        ]

    def get_output_names(self):
        return ['OUT']
