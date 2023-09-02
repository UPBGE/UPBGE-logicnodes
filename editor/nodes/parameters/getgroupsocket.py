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
    bl_icon = 'TRIA_RIGHT'
    nl_category = 'Nodes'
    nl_subcat = 'Groups'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicNodeGroup, 'Tree')
        self.add_input(NodeSocketLogicNodeGroupNode, 'Node Name')
        self.add_input(NodeSocketLogicIntegerPositive, "Input")
        self.add_output(NodeSocketLogicParameter, "Value")
        self.update_draw()

    def update_draw(self):
        if len(self.inputs) < 3:
            return
        tree = self.inputs[0]
        nde = self.inputs[1]
        ipt = self.inputs[2]
        if tree.is_linked or nde.is_linked:
            ipt.name = 'Input'
        if (tree.value or tree.is_linked) and (nde.value or nde.is_linked):
            ipt.enabled = True
        else:
            ipt.enabled = False
        if not tree.is_linked and not nde.is_linked and tree.value:
            tree_name = tree.value.name
            node_name = nde.value
            target = bpy.data.node_groups[tree_name].nodes.get(node_name)
            if not target or len(target.inputs) < 1:
                ipt.enabled = False
                return
            limit = len(target.inputs) - 1
            if int(ipt.value) > limit:
                ipt.value = limit
            name = target.inputs[ipt.value].name
            ipt.name = name

    def get_netlogic_class_name(self):
        return "ULGetNodeSocket"

    def get_input_names(self):
        return ["tree_name", 'node_name', "input_slot"]

    def get_output_names(self):
        return ['OUT']
