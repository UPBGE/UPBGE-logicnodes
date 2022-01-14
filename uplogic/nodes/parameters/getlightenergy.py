from uplogic.nodes import ULParameterNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting


class ULGetLightEnergy(ULParameterNode):

    def __init__(self):
        ULParameterNode.__init__(self)
        self.lamp = None
        self.energy = 0
        self.ENERGY = ULOutSocket(self, self.get_energy)

    def get_energy(self):
        lamp = self.get_input(self.lamp)
        if is_waiting(lamp):
            return STATUS_WAITING
        light = lamp.blenderObject.data
        return light.energy

    def evaluate(self):
        self._set_ready()
