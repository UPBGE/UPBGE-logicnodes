from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicNodeGroup
from ...sockets import NodeSocketLogicNodeGroupNode
from ...sockets import NodeSocketLogicIntegerPositive
import bpy


@node_type
class LogicNodeGetGroupSocket(LogicNodeParameterType):
    bl_idname = "NLGetNodeGroupNodeValue"
    bl_label = "Get Socket Value"
    bl_description = 'Get a socket value from a node in a node group'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetNodeSocket"

    def init(self, context):
        self.add_input(NodeSocketLogicNodeGroup, 'Tree', 'tree_name')
        self.add_input(NodeSocketLogicNodeGroupNode, 'Node Name', 'node_name')
        self.add_input(NodeSocketLogicIntegerPositive, "Input", 'input_slot')
        self.add_output(NodeSocketLogicParameter, "Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    def update_draw(self, context=None):
        if not self.ready:
            return
        tree = self.inputs[0]
        nde = self.inputs[1]
        ipt = self.inputs[2]
        if tree.is_linked or nde.is_linked:
            ipt.name = 'Input'
        if (tree.default_value or tree.is_linked) and (nde.default_value or nde.is_linked):
            ipt.enabled = True
        else:
            ipt.enabled = False
        if not tree.is_linked and not nde.is_linked and tree.default_value:
            tree_name = tree.default_value.name
            node_name = nde.default_value
            target = bpy.data.node_groups[tree_name].nodes.get(node_name)
            if not target or len(target.inputs) < 1:
                ipt.enabled = False
                return
            limit = len(target.inputs) - 1
            if int(ipt.default_value) > limit:
                ipt.default_value = limit
            name = target.inputs[ipt.default_value].name
            ipt.name = name

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["tree_name", 'node_name', "input_slot"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
