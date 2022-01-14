from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid


class ULExecuteSubNetwork(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.target_object = None
        self.tree_name = None
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
        target_object = self.get_input(self.target_object)
        tree_name = self.get_input(self.tree_name)
        self._set_ready()
        if is_invalid(target_object):
            return
        added_network = target_object.get(f'IGNLTree_{tree_name}', None)
        if not added_network:
            self._network.install_subnetwork(
                target_object,
                tree_name,
                False
            )
            added_network = target_object.get(f'IGNLTree_{tree_name}', None)
        if condition:
            added_network.stopped = False
        else:
            added_network.stop()
            added_network.stopped = True
            return
        self.done = True
