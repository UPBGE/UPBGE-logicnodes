from uplogic.events import catch
from uplogic.events import ULEvent
from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULCatchEvent(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.subject = None
        self.received = False
        self.event = None
        self.OUT = ULOutSocket(self, self.get_received)
        self.BODY = ULOutSocket(self, self.get_body)
        self.TARGET = ULOutSocket(self, self.get_target)

    def get_received(self):
        return isinstance(self.event, ULEvent)

    def get_body(self):
        return STATUS_WAITING if self.event is None else self.event.content

    def get_target(self):
        return STATUS_WAITING if self.event is None else self.event.messenger

    def evaluate(self):
        subject = self.get_input(self.subject)
        if is_invalid(subject):
            return
        self._set_ready()
        self.event = catch(subject)
        # print(self.event)
