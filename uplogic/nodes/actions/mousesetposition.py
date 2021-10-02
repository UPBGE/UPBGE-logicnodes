from uplogic.nodes import GEActionNode
from uplogic.nodes import GEOutSocket
from uplogic.nodes import is_waiting
from uplogic.nodes import not_met


class GESetMousePosition(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.screen_x = None
        self.screen_y = None
        self.network = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def setup(self, network):
        self.network = network

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        screen_x = self.get_socket_value(self.screen_x)
        screen_y = self.get_socket_value(self.screen_y)
        if is_waiting(screen_x, screen_y):
            return
        self._set_ready()
        self.network.set_mouse_position(screen_x, screen_y)
        self.done = True
