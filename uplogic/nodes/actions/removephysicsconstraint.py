from bge import constraints
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULRemovePhysicsConstraint(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.object = None
        self.name = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        obj = self.get_input(self.object)
        if is_invalid(obj):
            return
        name = self.get_input(self.name)
        if is_invalid(name):
            return
        self._set_ready()
        constraints.removeConstraint(obj[name].getConstraintId())
        self.done = True
