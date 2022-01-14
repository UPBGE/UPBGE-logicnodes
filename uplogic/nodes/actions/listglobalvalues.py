from uplogic.data import GlobalDB
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULListGlobalValues(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.data_id = None
        self.print_d = None
        self.gv_dict = None
        self.done = False
        self.OUT = ULOutSocket(self.get_done)
        self.VALUE = ULOutSocket(self.get_dict)

    def get_done(self):
        return self.done

    def get_dict(self):
        return self.gv_dict

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        data_id = self.get_input(self.data_id)
        print_d = self.get_input(self.print_d)
        if is_waiting(data_id, print_d):
            return
        self._set_ready()
        db = GlobalDB.retrieve(data_id)
        if print_d:
            print(f'[Logic Nodes] Global category "{data_id}":')
            for e in db.data:
                print('{}\t->\t{}'.format(e, db.data[e]))
            print('END ------------------------------------')
        self.done = True
        self.gv_dict = db.data
