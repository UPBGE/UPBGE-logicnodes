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
        socket = self.get_output('running')
        if socket is None:
            tree = self.tree
            if not tree:
                return STATUS_WAITING
            return self.set_output(
                'running',
                tree.is_running()
            )
        return socket

    def get_stopped(self):
        socket = self.get_output('stopped')
        if socket is None:
            tree = self.tree
            if not tree:
                return STATUS_WAITING
            return self.set_output(
                'stopped',
                tree.is_stopped()
            )
        return socket

    def evaluate(self):
        game_object = self.get_input(self.game_object)
        tree_name = self.get_input(self.tree_name)
        if is_waiting(game_object, tree_name):
            return
        self._set_ready()
        self._running = False
        self._stopped = False
        if is_invalid(game_object):
            return
        self.tree = game_object.get(f'IGNLTree_{tree_name}')
