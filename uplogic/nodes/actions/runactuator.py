from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULActionNode
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULRunActuator(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.game_obj = None
        self.cont_name = None
        self.act_name = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        game_obj = self.get_socket_value(self.game_obj)
        cont_name = self.get_socket_value(self.cont_name)
        act_name = self.get_socket_value(self.act_name)
        if is_waiting(act_name, cont_name):
            return
        controller = game_obj.controllers[cont_name]
        if act_name not in controller.actuators:
            return
        actuator = controller.actuators[act_name]
        condition = self.get_socket_value(self.condition)
        self._set_ready()
        if not_met(condition):
            controller.deactivate(actuator)
            return
        controller.activate(actuator)
        self.done = True
