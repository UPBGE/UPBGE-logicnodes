from uplogic.nodes import GEActionNode
from uplogic.nodes import GEOutSocket
from uplogic.nodes import Invalid
from uplogic.nodes import is_invalid
from uplogic.nodes import is_waiting
from uplogic.nodes import not_met


class GETrowEvent(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.subject = None
        self.body = None
        self.target = None
        self.old_subject = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        osubject = self.old_subject
        events = self.network._events
        if not_met(condition):
            if osubject in events.data:
                if events.data[osubject][2] is self:
                    events.pop(osubject, None)
            self._set_ready()
            return
        subject = self.get_socket_value(self.subject)
        self.old_subject = subject
        body = self.get_socket_value(self.body)
        if isinstance(body, Invalid):
            body = None
        target = self.get_socket_value(self.target)
        if is_waiting(body, target):
            return
        if is_invalid(subject):
            return
        self._set_ready()
        events.put(subject, [body, target, self], False)
        self.done = True
