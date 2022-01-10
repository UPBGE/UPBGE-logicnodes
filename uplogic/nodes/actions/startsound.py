from uplogic.audio import ULSound2D
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_invalid
from uplogic.utils import not_met


class ULStartSound(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.sound = None
        self.loop_count = None
        self.pitch = None
        self.volume = None
        self.done = None
        self.device = None
        self.on_finish = False
        self._handle = None
        self.DONE = ULOutSocket(self, self.get_done)
        self.ON_FINISH = ULOutSocket(self, self.get_on_finish)
        self.HANDLE = ULOutSocket(self, self.get_handle)

    def get_handle(self):
        return self._handle

    def get_on_finish(self):
        if not self._handle:
            return False
        if self._handle.finished:
            self._handle = None
            return True
        return False

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        self.on_finish = False
        self._set_ready()
        condition = self.get_input(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        pitch = self.get_input(self.pitch)
        volume = self.get_input(self.volume)
        file = self.get_input(self.sound)
        loop_count = self.get_input(self.loop_count)

        if is_invalid(file):
            return

        self._handle = ULSound2D(
            file,
            'default',
            volume,
            pitch,
            loop_count
        )
