from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicMaterial
from ...sockets import NodeSocketLogicTreeNode


@node_type
class LogicNodeGetMatNode(LogicNodeParameterType):
    bl_idname = "NLGetMaterialNode"
    bl_label = "Get Node"
    bl_description = 'A shader node'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetMaterialNode"

    def init(self, context):
        self.add_input(NodeSocketLogicMaterial, 'Material', 'mat_name')
        self.add_input(NodeSocketLogicTreeNode, 'Node Name', 'node_name')
        self.add_output(NodeSocketLogicParameter, "Node", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["mat_name", 'node_name']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
