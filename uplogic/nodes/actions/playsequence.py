from uplogic.animation.sequence import ULSequence
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULPaySequence(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.mat_name = None
        self.node_name = None
        self.play_mode = None
        self.play_continue = None
        self.frames = None
        self.sequence = None
        self.fps = None
        self.ON_START = ULOutSocket(self, self._get_on_start)
        self.RUNNING = ULOutSocket(self, self._get_running)
        self.ON_FINISH = ULOutSocket(self, self._get_on_finish)
        self.FRAME = ULOutSocket(self, self._get_frame)

    def _get_on_start(self):
        return self.on_start

    def _get_running(self):
        return getattr(self.sequence.running, False)

    def _get_on_finish(self):
        return self.on_finish

    def _get_frame(self):
        return self.frame

    def evaluate(self):
        self.on_finish = False
        self.on_start = False
        condition = self.get_input(self.condition)
        play_continue = self.get_input(self.play_continue)
        if self.sequence:
            if self.sequence.on_finish:
                self.on_finish = True
                if self.sequence.mode < 3:
                    self.sequence = None
        play_mode = self.get_input(self.play_mode)
        frames = self.get_input(self.frames)
        if not_met(condition) and play_mode < 2:
            return
        elif not_met(condition) and self.sequence:
            if not play_continue:
                self.sequence.restart()
            self.sequence.pause()
        elif condition and self.sequence:
            self.sequence.unpause()
        mat_name = self.get_input(self.mat_name)
        node_name = self.get_input(self.node_name)
        fps = self.get_input(self.fps)
        if is_waiting(
            mat_name,
            node_name,
            play_mode,
            frames,
            fps
        ):
            return
        if not self.sequence:
            if play_mode > 2:
                play_mode -= 3
            self.sequence = ULSequence(
                mat_name,
                node_name,
                frames.x,
                frames.y,
                fps,
                play_mode
            )
