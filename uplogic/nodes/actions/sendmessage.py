from uplogic.nodes import ULActionNode
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULSendMessage(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.from_obj = None
        self.to_obj = None
        self.subject = None
        self.body = None

    def evaluate(self):
        condition = self.get_input(self.condition)
        if not_met(condition):
            self._set_ready()
            self._set_value(False)
            return
        from_obj = self.get_input(self.from_obj)
        to_obj = self.get_input(self.to_obj)
        subject = self.get_input(self.subject)
        body = self.get_input(self.body)
        if is_waiting(from_obj, to_obj, subject, body):
            return
        self._set_ready()
        if body and to_obj:
            from_obj.sendMessage(subject, body=body, to=to_obj)
        elif body:
            from_obj.sendMessage(subject, body=body)
        elif to_obj:
            from_obj.sendMessage(subject, to=to_obj)
        else:
            from_obj.sendMessage(subject)
        self._set_value(True)
