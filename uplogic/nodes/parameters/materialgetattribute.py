from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
import bpy


class ULGetMaterialAttribute(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.mat_name = None
        self.node_name = None
        self.internal = None
        self.attribute = None
        self.OUT = ULOutSocket(self, self._get_val)

    def _get_val(self):
        socket = self.get_output('val')
        if socket is None:
            mat_name = self.get_input(self.mat_name)
            node_name = self.get_input(self.node_name)
            if is_invalid(mat_name, node_name):
                return STATUS_WAITING
            internal = self.get_input(self.internal)
            attribute = self.get_input(self.attribute)
            if is_waiting(mat_name):
                return STATUS_WAITING
            target = (
                bpy.data.materials[mat_name]
                .node_tree
                .nodes[node_name]
            )
            if internal:
                target = getattr(target, internal, target)
            return self.set_output(
                'val',
                getattr(target, attribute, None)
            )
        return socket

    def evaluate(self):
        self._set_ready()
