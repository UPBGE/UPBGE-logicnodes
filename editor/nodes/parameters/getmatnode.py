from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicMaterial
from ...sockets import NodeSocketLogicTreeNode


@node_type
class LogicNodeGetMatNode(LogicNodeParameterType):
    bl_idname = "NLGetMaterialNode"
    bl_label = "Get Node"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULGetMaterialNode"

    def init(self, context):
        self.add_input(NodeSocketLogicMaterial, 'Material')
        self.add_input(NodeSocketLogicTreeNode, 'Node Name')
        self.add_output(NodeSocketLogicParameter, "Node")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["mat_name", 'node_name']

    def get_output_names(self):
        return ['OUT']
