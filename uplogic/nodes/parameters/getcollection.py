from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULGetCollection(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.collection = None
        self.OUT = ULOutSocket(self, self.get_collection)

    def get_collection(self):
        collection = self.get_input(self.collection)
        if is_invalid(collection):
            return STATUS_WAITING
        return collection

    def evaluate(self):
        self._set_ready()
