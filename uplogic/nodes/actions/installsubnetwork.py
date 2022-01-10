from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULInstallSubNetwork(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.target_object = None
        self.tree_name = None
        self.initial_status = None
        self._network = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def setup(self, network):
        self._network = network

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        target_object = self.get_input(self.target_object)
        tree_name = self.get_input(self.tree_name)
        initial_status = self.get_input(self.initial_status)
        if is_waiting(
            target_object,
            tree_name,
            initial_status
        ):
            return
        self._set_ready()
        if is_invalid(target_object):
            return
        self._network.install_subnetwork(
            target_object,
            tree_name,
            initial_status
        )
        self.done = True
