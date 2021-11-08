from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING, is_invalid
from uplogic.utils import is_waiting


class ULLogicTreeStatus(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.game_object = None
        self.tree_name = None
        self._running = False
        self._stopped = False
        self.tree = None
        self.IFRUNNING = ULOutSocket(self, self.get_running)
        self.IFSTOPPED = ULOutSocket(self, self.get_stopped)

    def get_running(self):
        tree = self.tree
        if not tree:
            return STATUS_WAITING
        return tree.is_running()

    def get_stopped(self):
        tree = self.tree
        if not tree:
            return STATUS_WAITING
        return tree.is_stopped()

    def evaluate(self):
        game_object = self.get_socket_value(self.game_object)
        tree_name = self.get_socket_value(self.tree_name)
        if is_waiting(game_object, tree_name):
            return
        self._set_ready()
        self._running = False
        self._stopped = False
        if is_invalid(game_object):
            return
        self.tree = game_object.get(f'IGNLTree_{tree_name}')
