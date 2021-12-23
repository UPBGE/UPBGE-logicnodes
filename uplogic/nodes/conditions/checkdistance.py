from uplogic.nodes import ULConditionNode
from uplogic.utils import LOGIC_OPERATORS
from uplogic.utils import is_invalid
from uplogic.utils import is_waiting
from uplogic.utils import compute_distance


class ULCheckDistance(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.param_a = None
        self.param_b = None
        self.operator = None
        self.dist = None
        self.hyst = None
        self._check = self._strict_check

    def _strict_check(self, opindex, value, hyst, threshold):
        v = LOGIC_OPERATORS[opindex](value, threshold)
        if v is True:
            self._set_value(True)
        else:
            self._set_value(False)
            self._check = self._hyst_check

    def _hyst_check(self, opindex, value, hyst, threshold):
        if (opindex == 2) or (opindex == 4):
            v = LOGIC_OPERATORS[opindex](value, threshold + hyst)
            if v is True:
                self._set_value(True)
                self._check = self._strict_check
            else:
                self._set_value(False)
        elif (opindex == 3) or (opindex == 5):
            v = LOGIC_OPERATORS[opindex](value, threshold - hyst)
            if v is True:
                self._set_value(True)
                self._check = self._strict_check
            else:
                self._set_value(False)

    def evaluate(self):
        a = self.get_socket_value(self.param_a)
        b = self.get_socket_value(self.param_b)
        op = self.get_socket_value(self.operator)
        dist = self.get_socket_value(self.dist)
        hyst = self.get_socket_value(self.hyst)
        if is_waiting(a, b, op, dist, hyst):
            return
        self._set_ready()
        if is_invalid(a):
            return
        if is_invalid(b):
            return
        if op is None:
            return
        if dist is None:
            return
        distance = compute_distance(a, b)
        if distance is None:
            return self._set_value(False)
        if hyst is None:  # plain check, no threshold
            v = LOGIC_OPERATORS[op](distance, dist)
            self._set_value(v)
        else:  # check with hysteresys value, if >, >=, <, <=
            self._check(op, distance, hyst, dist)
