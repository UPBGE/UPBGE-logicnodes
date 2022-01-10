from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import not_met
import bpy


class ULSetNodeSocket(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.tree_name = None
        self.node_name = None
        self.input_slot = None
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
        input_slot = self.get_input(self.input_slot)
        value = self.get_input(self.value)
        if is_waiting(node_name, input_slot, value):
            return
        if is_invalid(tree_name):
            return
        if condition:
            self.done = True
            self._set_ready()
            (
                bpy.data.node_groups[tree_name]
                .nodes[node_name]
                .inputs[input_slot]
                .default_value
            ) = value
