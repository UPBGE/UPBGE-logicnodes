from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import not_met
import bpy


class ULSetNodeValue(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.tree_name = None
        self.node_name = None
        self.internal = None
        self.attribute = None
        self.value = None
        self.done = False
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        tree_name = self.get_input(self.tree_name)
        node_name = self.get_input(self.node_name)
        attribute = self.get_input(self.attribute)
        internal = self.get_input(self.internal)
        value = self.get_input(self.value)
        if is_waiting(node_name, attribute, internal, value):
            return
        if is_invalid(tree_name):
            return
        if condition:
            self._set_ready()
            target = (
                bpy
                .data
                .node_groups[tree_name]
                .nodes[node_name]
            )
            if internal:
                target = getattr(target, internal, target)
            if hasattr(target, attribute):
                setattr(target, attribute, value)
            self.done = True
