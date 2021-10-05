from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_INVALID
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULTrowEvent(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.subject = None
        self.body = None
        self.target = None
        self.old_subject = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

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
        if body is STATUS_INVALID:
            body = None
        target = self.get_socket_value(self.target)
        if is_waiting(body, target):
            return
        if is_invalid(subject):
            return
        self._set_ready()
        events.put(subject, [body, target, self], False)
        self.done = True
