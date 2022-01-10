from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
import bpy


class ULGetMaterialSocket(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.mat_name = None
        self.node_name = None
        self.input_slot = None
        self.OUT = ULOutSocket(self, self._get_val)

    def _get_val(self):
        socket = self.get_output('val')
        if socket is None:
            mat_name = self.get_input(self.mat_name)
            node_name = self.get_input(self.node_name)
            if is_invalid(mat_name, node_name):
                return STATUS_WAITING
            input_slot = self.get_input(self.input_slot)
            if is_waiting(mat_name):
                return STATUS_WAITING
            return self.set_output(
                'val',
                (
                    bpy.data.materials[mat_name]
                    .node_tree
                    .nodes[node_name]
                    .inputs[input_slot]
                    .default_value
                )
            )
        return socket

    def evaluate(self):
        self._set_ready()
