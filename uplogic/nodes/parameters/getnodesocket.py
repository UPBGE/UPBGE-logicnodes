from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
import bpy


class ULGetNodeSocket(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.tree_name = None
        self.node_name = None
        self.input_slot = None
        self.OUT = ULOutSocket(self, self._get_val)

    def _get_val(self):
        socket = self.get_output('val')
        if socket is None:
            tree_name = self.get_input(self.tree_name)
            node_name = self.get_input(self.node_name)
            if is_invalid(tree_name, node_name):
                return STATUS_WAITING
            input_slot = self.get_input(self.input_slot)
            if is_waiting(tree_name):
                return STATUS_WAITING
            return self.set_output(
                'val',
                (
                    bpy.data
                    .node_groups[tree_name]
                    .nodes[node_name]
                    .inputs[input_slot]
                    .default_value
                )
            )
        return socket

    def evaluate(self):
        self._set_ready()
