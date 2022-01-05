from bge import logic
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULAddObject(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.name = None
        self.reference = None
        self.life = None
        self.done = False
        self.obj = False
        self.OBJ = ULOutSocket(self, self._get_obj)
        self.OUT = ULOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def _get_obj(self):
        return self.obj

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        life = self.get_socket_value(self.life)
        name = self.get_socket_value(self.name)
        self._set_ready()
        reference = self.get_socket_value(self.reference)
        scene = logic.getCurrentScene()
        if is_waiting(life, name, reference):
            return
        self.obj = scene.addObject(name, reference, life)
        self.done = True
