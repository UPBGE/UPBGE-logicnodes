from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
import bpy


class ULGetMaterialNode(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.mat_name = None
        self.node_name = None
        self.OUT = ULOutSocket(self, self._get_val)

    def _get_val(self):
        mat_name = self.get_input(self.mat_name)
        node_name = self.get_input(self.node_name)
        if is_invalid(mat_name, node_name):
            return STATUS_WAITING
        return (
            bpy.data.materials[mat_name]
            .node_tree
            .nodes[node_name]
        )

    def evaluate(self):
        self._set_ready()
