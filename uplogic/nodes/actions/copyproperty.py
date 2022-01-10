from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULCopyProperty(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.from_object = None
        self.to_object = None
        self.property_name = None
        self.done = False
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        from_object = self.get_input(self.from_object)
        to_object = self.get_input(self.to_object)
        if is_invalid(from_object, to_object):
            return
        property_name = self.get_input(self.property_name)
        if is_waiting(property_name):
            return
        self._set_ready()
        val = from_object.get(property_name)
        if val is not None:
            to_object[property_name] = val
            self.done = True
