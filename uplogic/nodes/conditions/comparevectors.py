from mathutils import Vector
from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import LOGIC_OPERATORS
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting


class ULCompareVectors(ULConditionNode):
    def __init__(self, operator='GREATER'):
        ULConditionNode.__init__(self)
        self.operator = operator
        self.all = None
        self.threshold = None
        self.param_a = None
        self.param_b = None
        self.OUT = ULOutSocket(self, self.get_result)

    def get_result(self):
        socket = self.get_output('result')
        if socket is None:
            a = self.get_input(self.param_a)
            b = self.get_input(self.param_b)
            all_values = self.get_input(self.all)
            operator = self.get_input(self.operator)
            threshold = self.get_input(self.threshold)
            if is_waiting(a, b, all_values, operator, threshold):
                return STATUS_WAITING
            if (
                not isinstance(a, Vector)
                or not isinstance(b, Vector)
            ):
                return STATUS_WAITING
            if operator > 1:  # eq and neq are valid for None
                if a is None:
                    return STATUS_WAITING
                if b is None:
                    return STATUS_WAITING
            if operator is None:
                return STATUS_WAITING
            return self.set_output(
                'result',
                self.get_vec_val(
                    operator,
                    a,
                    b,
                    all_values,
                    threshold
                )
            )
        return socket

    def get_vec_val(self, op, a, b, xyz, threshold):
        for ax in ['x', 'y', 'z']:
            av = getattr(a, ax)
            bv = getattr(b, ax)
            av = bv if abs(av - bv) < threshold else av
            if xyz[ax] and not LOGIC_OPERATORS[op](av, bv):
                return False
        return True

    def evaluate(self):
        self._set_ready()
