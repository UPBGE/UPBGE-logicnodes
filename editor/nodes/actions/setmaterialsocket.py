from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicMaterial
from ...sockets import NodeSocketLogicTreeNode
import bpy


@node_type
class LogicNodeSetMaterialSocket(LogicNodeActionType):
    bl_idname = "NLSetMaterialNodeValue"
    bl_label = "Set Socket"
    bl_description = 'Set a socket value of a material node'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetMatNodeSocket"

    search_tags = [
        ['Set Material Socket', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicMaterial, 'Material', 'mat_name')
        self.add_input(NodeSocketLogicTreeNode, 'Node Name', 'node_name', {'ref_index': 1})
        self.add_input(NodeSocketLogicIntegerPositive, "Input", 'input_slot')
        self.add_input(NodeSocketLogicFloat, 'Value', 'value')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        LogicNodeActionType.init(self, context)

    def update_draw(self, context=None):
        if not self.ready:
            return
        mat = self.inputs[1]
        nde = self.inputs[2]
        ipt = self.inputs[3]
        val = self.inputs[4]
        if mat.is_linked or nde.is_linked:
            ipt.name = 'Input'
        if (mat.default_value or mat.is_linked) and (nde.default_value or nde.is_linked):
            ipt.enabled = val.enabled = True
        else:
            ipt.enabled = val.enabled = False
        if not mat.is_linked and not nde.is_linked and mat.default_value:
            mat_name = mat.default_value.name
            node_name = nde.default_value
            target = bpy.data.materials[mat_name].node_tree.nodes[node_name]
            limit = len(target.inputs) - 1
            if int(ipt.default_value) > limit:
                ipt.default_value = limit
            name = target.inputs[ipt.default_value].name
            ipt.name = name

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "mat_name",
            'node_name',
            "input_slot",
            'value'
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
