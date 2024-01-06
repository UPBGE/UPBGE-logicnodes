from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicGeometryNodeTree
from ...sockets import NodeSocketLogicGeometryNodeTree
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicFloat
import bpy


@node_type
class LogicNodeSetGeometrySocket(LogicNodeActionType):
    bl_idname = "NLSetGeometryNodeValue"
    bl_label = "Set Socket"
    nl_module = 'uplogic.nodes.actions'
    # deprecated = True

    search_tags = [
        ['Set Geometry Socket', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicGeometryNodeTree, 'Tree')
        self.add_input(NodeSocketLogicGeometryNodeTree, 'Node Name', None, {'ref_index': 1})
        self.add_input(NodeSocketLogicIntegerPositive, "Input")
        self.add_input(NodeSocketLogicFloat, 'Value')
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def update_draw(self, context=None):
        tree = self.inputs[1]
        nde = self.inputs[2]
        ipt = self.inputs[3]
        val = self.inputs[4]
        if tree.is_linked or nde.is_linked:
            ipt.name = 'Input'
        if (tree.default_value or tree.is_linked) and (nde.default_value or nde.is_linked):
            ipt.enabled = val.enabled = True
        else:
            ipt.enabled = val.enabled = False
        if not tree.is_linked and not nde.is_linked and tree.default_value:
            tree_name = tree.default_value.name
            node_name = nde.default_value
            target = bpy.data.node_groups[tree_name].nodes[node_name]
            limit = len(target.inputs) - 1
            if int(ipt.default_value) > limit:
                ipt.default_value = limit
            name = target.inputs[ipt.default_value].name
            ipt.name = name

    nl_class = "ULSetNodeSocket"

    def get_input_names(self):
        return [
            "condition",
            "tree_name",
            'node_name',
            "input_slot",
            'value'
        ]

    def get_output_names(self):
        return ['OUT']
