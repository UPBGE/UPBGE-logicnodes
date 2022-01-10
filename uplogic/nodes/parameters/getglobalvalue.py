from uplogic.data import GlobalDB
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_INVALID
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting


class ULGetGlobalValue(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.data_id = None
        self.key = None
        self.default = None
        self.OUT = ULOutSocket(self, self.get_out)

    def get_out(self):
        socket = self.get_output('val')
        if socket is None:
            data_id = self.get_input(self.data_id)
            key = self.get_input(self.key)
            default = self.get_input(self.default)
            if default is STATUS_INVALID:
                default = None
            if is_waiting(data_id, key, default):
                return STATUS_WAITING
            db = GlobalDB.retrieve(data_id)
            return self.set_output('val', db.get(key, default))
        return socket

    def evaluate(self):
        self._set_ready()
