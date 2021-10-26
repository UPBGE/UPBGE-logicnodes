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
        data_id = self.get_socket_value(self.data_id)
        key = self.get_socket_value(self.key)
        default = self.get_socket_value(self.default)
        if default is STATUS_INVALID:
            default = None
        if is_waiting(data_id, key, default):
            return STATUS_WAITING
        db = GlobalDB.retrieve(data_id)
        return db.get(key, default)

    def evaluate(self):
        self._set_ready()
