from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULHasProperty(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.game_object = None
        self.property_name = None
        self.OUT = ULOutSocket(self, self.get_stat)

    def get_stat(self):
        game_object = self.get_socket_value(self.game_object)
        property_name = self.get_socket_value(self.property_name)
        if is_invalid(game_object, property_name):
            return STATUS_WAITING
        return (
            True if property_name in game_object.getPropertyNames()
            else False
        )

    def evaluate(self):
        self._set_ready()
