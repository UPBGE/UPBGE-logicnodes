from uplogic.nodes import ULActionNode
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULSetPyInstanceAttr(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.instance = None
        self.attr = None
        self.value = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        instance = self.get_socket_value(self.instance)
        attr = self.get_socket_value(self.attr)
        value = self.get_socket_value(self.value)
        if is_waiting(instance, attr, value):
            return
        self._set_ready()
        setattr(instance, attr, value)
