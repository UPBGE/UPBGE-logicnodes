from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULChildByName(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.from_parent = None
        self.child = None
        self.CHILD = ULOutSocket(self, self.get_child)

    def get_child(self):
        socket = self.get_output('child')
        if socket is None:
            parent = self.get_input(self.from_parent)
            child_name = self.get_input(self.child)
            if is_invalid(parent, child_name):
                return STATUS_WAITING
            return self.set_output(
                'child',
                parent.childrenRecursive.get(child_name)
            )
        return socket

    def evaluate(self):
        self._set_ready()
