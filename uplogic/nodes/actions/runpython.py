from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_INVALID
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULRunPython(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.module_name = None
        self.module_func = None
        self.arg = None
        self.val = None
        self.OUT = ULOutSocket(self, self.get_done)
        self.VAL = ULOutSocket(self, self.get_val)
        self._old_mod_name = None
        self._old_mod_fun = None
        self._module = None
        self._modfun = None

    def get_done(self):
        return self.done

    def get_val(self):
        return self.val

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        mname = self.get_input(self.module_name)
        mfun = self.get_input(self.module_func)
        if is_waiting(mname, mfun):
            return
        arg = self.get_input(self.arg)
        self._set_ready()
        if mname and (self._old_mod_name != mname):
            exec("import {}".format(mname))
            self._old_mod_name = mname
            self._module = eval(mname)
        if self._old_mod_fun != mfun:
            self._modfun = getattr(self._module, mfun)
            self._old_mod_fun = mfun
        if arg is STATUS_INVALID:
            self.val = self._modfun()
        else:
            self.val = self._modfun(arg)
        self.done = True
