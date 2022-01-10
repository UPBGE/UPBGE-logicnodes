from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
import math


class ULFormula(ULParameterNode):

    @classmethod
    def signum(cls, a):
        return (a > 0) - (a < 0)

    @classmethod
    def curt(cls, a):
        if a > 0:
            return a**(1./3.)
        else:
            return -(-a)**(1./3.)

    def __init__(self):
        ULParameterNode.__init__(self)
        self.a = None
        self.b = None
        self.formula = ""
        self._formula_globals = globals()
        self._formula_locals = {
            "exp": math.exp,
            "pow": math.pow,
            "log": math.log,
            "log10": math.log10,
            "acos": math.acos,
            "asin": math.asin,
            "atan": math.atan,
            "atan2": math.atan2,
            "cos": math.cos,
            "hypot": math.hypot,
            "sin": math.sin,
            "tan": math.tan,
            "degrees": math.degrees,
            "radians": math.radians,
            "acosh": math.acosh,
            "asinh": math.asinh,
            "atanh": math.atanh,
            "cosh": math.cosh,
            "sinh": math.sinh,
            "tanh": math.tanh,
            "pi": math.pi,
            "e": math.e,
            "ceil": math.ceil,
            "sign": ULFormula.signum,
            "abs": math.fabs,
            "floor": math.floor,
            "mod": math.fmod,
            "sqrt": math.sqrt,
            "curt": ULFormula.curt,
            "str": str,
            "int": int,
            "float": float
        }
        self.OUT = ULOutSocket(self, self.get_out)

    def get_out(self):
        socket = self.get_output('out')
        if socket is None:
            a = self.get_input(self.a)
            b = self.get_input(self.b)
            formula_locals = self._formula_locals
            formula_locals["a"] = a
            formula_locals["b"] = b
            out = eval(self.formula, self._formula_globals, formula_locals)
            return self.set_output('out', out)
        return socket

    def evaluate(self):
        self._set_ready()
