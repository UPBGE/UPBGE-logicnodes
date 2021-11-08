from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULConditionNode
from uplogic.utils import LOGIC_OPERATORS
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting


class ULEvaluateProperty(ULConditionNode):
    def __init__(self, operator='EQUAL'):
        ULConditionNode.__init__(self)
        self.game_object = None
        self.property_name = None
        self.operator = operator
        self.compare_value = None
        self.OUT = ULOutSocket(self, self.get_out)
        self.val = 0
        self.VAL = ULOutSocket(self, self.get_val)

    def get_out(self):
        compare_value = self.get_socket_value(self.compare_value)
        if is_waiting(compare_value):
            return STATUS_WAITING
        operator = self.get_socket_value(self.operator)
        if operator > 1:  # eq and neq are valid for None
            if is_invalid(self.val, compare_value):
                return STATUS_WAITING
        if operator is None:
            return STATUS_WAITING
        return LOGIC_OPERATORS[operator](self.val, compare_value)

    def get_val(self):
        return self.val

    def evaluate(self):
        game_object = self.get_socket_value(self.game_object)
        if is_invalid(game_object):
            return STATUS_WAITING
        property_name = self.get_socket_value(self.property_name)
        if is_waiting(property_name):
            return STATUS_WAITING
        self._set_ready()
        self.val = game_object[property_name]
