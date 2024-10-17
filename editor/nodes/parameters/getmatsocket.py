from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicTreeNode
from ...sockets import NodeSocketLogicMaterial
from ...sockets import NodeSocketLogicIntegerPositive
import bpy


@node_type
class LogicNodeGetMaterialSocket(LogicNodeParameterType):
    bl_idname = "NLGetMaterialNodeValue"
    bl_label = "Get Socket Value"
    bl_description = 'A socket value of a shader node'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetMaterialSocket"

    def init(self, context):
        self.add_input(NodeSocketLogicMaterial, 'Material', 'mat_name')
        self.add_input(NodeSocketLogicTreeNode, 'Node Name', 'node_name')
        self.add_input(NodeSocketLogicIntegerPositive, "Input", 'input_slot')
        self.add_output(NodeSocketLogicParameter, "Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    def update_draw(self, context=None):
        if not self.ready:
            return
        mat = self.inputs[0]
        nde = self.inputs[1]
        ipt = self.inputs[2]
        if mat.is_linked or nde.is_linked:
            ipt.name = 'Input'
        if (mat.default_value or mat.is_linked) and (nde.default_value or nde.is_linked):
            ipt.enabled = True
        else:
            ipt.enabled = False
        if not mat.is_linked and not nde.is_linked and mat.default_value:
            mat_name = mat.default_value.name
            node_name = nde.default_value
            target = bpy.data.materials[mat_name].node_tree.nodes.get(node_name)
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
        return ["mat_name", 'node_name', "input_slot"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
