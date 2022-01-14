from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULSetParent(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.child_object = None
        self.parent_object = None
        self.compound = True
        self.ghost = True
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        child_object = self.get_input(self.child_object)
        parent_object = self.get_input(self.parent_object)
        compound = self.get_input(self.compound)
        ghost = self.get_input(self.ghost)
        self._set_ready()
        if is_invalid(child_object, parent_object, compound, ghost):
            return
        if child_object.parent is parent_object:
            return
        child_object.setParent(parent_object, compound, ghost)
        self.done = True
