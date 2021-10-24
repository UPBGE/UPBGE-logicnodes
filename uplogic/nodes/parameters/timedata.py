from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_READY


class ULTimeData(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.network = None
        self.TIME_PER_FRAME = ULOutSocket(
            self,
            self.get_time_per_frame
        )
        self.FPS = ULOutSocket(self, self.get_fps)
        self.TIMELINE = ULOutSocket(self, self.get_timeline)

    def get_time_per_frame(self):
        return self.network.time_per_frame

    def get_fps(self):
        tpf = self.network.time_per_frame
        if not tpf:
            return 1
        fps = (1 / tpf)
        return fps

    def get_timeline(self):
        return self.network.timeline

    def setup(self, network):
        self.network = network

    def has_status(self, status):
        return status is STATUS_READY

    def evaluate(self):
        pass
