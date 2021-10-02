from uplogic.nodes import GEOutSocket
from uplogic.nodes import GEParameterNode
from uplogic.nodes import is_invalid


class GECatchEvent(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.subject = None
        self.received = False
        self.event = [None, None]
        self.OUT = GEOutSocket(self, self.get_received)
        self.BODY = GEOutSocket(self, self.get_body)
        self.TARGET = GEOutSocket(self, self.get_target)

    def get_received(self):
        return self.received

    def get_body(self):
        return self.event[0]

    def get_target(self):
        return self.event[1]

    def evaluate(self):
        self.received = False
        subject = self.get_socket_value(self.subject)
        if is_invalid(subject):
            return
        self._set_ready()
        events = self.network._events
        if subject in events.data:
            self.received = True
            self.event = events.data[subject]
